import gradio as gr
import pandas as pd
import numpy as np
import xgboost as xgb
from thundergbm import TGBMClassifier
from scipy import sparse
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score
import os
import time

CACHE_PATH = "/root/ieee_preprocessed.pkl"

# -------------------------
# AMD UI colors
# -------------------------
AMD_TEAL = "#00C2DE"
AMD_BLACK = "#1C1C1C"
TEXT_WHITE = "#FFFFFF"


# -------------------------
# Load & preprocess data
# -------------------------
def load_and_preprocess():
    if os.path.exists(CACHE_PATH):
        print("Loading cached preprocessed dataset…")
        return pd.read_pickle(CACHE_PATH)

    trans_path = "/root/train_transaction.csv"
    ident_path = "/root/train_identity.csv"

    if not os.path.exists(trans_path):
        raise FileNotFoundError("Missing file: train_transaction.csv")
    if not os.path.exists(ident_path):
        raise FileNotFoundError("Missing file: train_identity.csv")

    print("Loading transaction data…")
    train_transaction = pd.read_csv(trans_path, low_memory=False)

    print("Loading identity data…")
    train_identity = pd.read_csv(ident_path, low_memory=False)

    print("Merging datasets…")
    df = train_transaction.merge(
        train_identity,
        on="TransactionID",
        how="left",
        sort=False,
        copy=False
    )

    print("Encoding categorical features…")
    cat_cols = df.select_dtypes(include=["object", "category"]).columns
    for col in cat_cols:
        df[col], _ = pd.factorize(df[col], sort=False)

    df = df.fillna(0).astype(np.float32)

    print("Saving preprocessed cache…")
    df.to_pickle(CACHE_PATH)

    return df


# -------------------------
# Train XGBoost (CPU) and ThunderGBM (GPU)
# -------------------------
def train_model(max_depth, n_estimators, learning_rate):
    try:
        df = load_and_preprocess()
    except Exception as e:
        return str(e), 0, 0, None, None, None

    if "isFraud" not in df.columns:
        return "ERROR: 'isFraud' not found.", 0, 0, None, None, None

    y = df["isFraud"]
    X = df.drop(columns=["isFraud"])

    split_idx = int(len(df) * 0.8)
    X_train = X.iloc[:split_idx]
    y_train = y.iloc[:split_idx]
    X_test = X.iloc[split_idx:]
    y_test = y.iloc[split_idx:]
    transaction_ids_test = df["TransactionID"].iloc[split_idx:]

    # ============================================================
    # XGBOOST CPU
    # ============================================================
    print("\n===== XGBOOST CPU TRAINING =====")
    xgb_model = xgb.XGBClassifier(
        tree_method="hist",
        n_estimators=int(n_estimators),
        max_depth=int(max_depth),
        learning_rate=float(learning_rate),
        subsample=0.8,
        colsample_bytree=0.8,
        n_jobs=-1
    )

    cpu_start = time.time()
    xgb_model.fit(X_train, y_train)
    cpu_time = time.time() - cpu_start

    xgb_preds = xgb_model.predict_proba(X_test)[:, 1]
    xgb_preds_labels = (xgb_preds > 0.5).astype(int)

    cpu_auc = roc_auc_score(y_test, xgb_preds)
    cpu_acc = accuracy_score(y_test, xgb_preds_labels)
    cpu_precision = precision_score(y_test, xgb_preds_labels)
    cpu_recall = recall_score(y_test, xgb_preds_labels)

    # ============================================================
    # THUNDERGBM GPU
    # ============================================================
    print("\n===== THUNDERGBM GPU TRAINING =====")
    X_train_sparse = sparse.csr_matrix(X_train.values)
    X_test_sparse = sparse.csr_matrix(X_test.values)

    tgbm_model = TGBMClassifier(
        depth=int(max_depth),
        n_trees=int(n_estimators),
        learning_rate=float(learning_rate),
        objective="binary:logistic",
        lambda_tgbm=2.0,
        max_num_bin=64,
        min_child_weight=10,
        verbose=1,
        n_gpus=1
    )

    gpu_start = time.time()
    tgbm_model.fit(X_train_sparse, y_train)
    gpu_time = time.time() - gpu_start

    gpu_preds = tgbm_model.predict(X_test_sparse)

    gpu_auc = roc_auc_score(y_test, gpu_preds)
    gpu_acc = accuracy_score(y_test, gpu_preds)
    gpu_precision = precision_score(y_test, gpu_preds)
    gpu_recall = recall_score(y_test, gpu_preds)

    # ============================================================
    # Speedup Calculation
    # ============================================================
    speedup = cpu_time / gpu_time if gpu_time > 0 else 0

    # ============================================================
    # Prediction Table (GPU Model)
    # ============================================================
    results_df = pd.DataFrame({
        "TransactionID": transaction_ids_test.values,
        "Test Fraud Probability": y_test.values,
        "Fraud Probability": gpu_preds
    }).sort_values(by="Test Fraud Probability", ascending=False)

    top_preds_df = results_df.head(20).reset_index(drop=True)
    full_preds_df = results_df.reset_index(drop=True)

    # ============================================================
    # Output Text
    # ============================================================
    status_msg = (
        f"Training complete!\n\n"

        f"====== XGBOOST CPU RESULTS ======\n"
        f"Runtime: {cpu_time:.3f} sec\n"
        f"AUC: {cpu_auc:.5f}\n"
        f"Accuracy: {cpu_acc:.5f}\n"
        f"Precision: {cpu_precision:.5f}\n"
        f"Recall: {cpu_recall:.5f}\n\n"

        f"====== THUNDERGBM GPU RESULTS ======\n"
        f"Runtime: {gpu_time:.3f} sec\n"
        f"AUC: {gpu_auc:.5f}\n"
        f"Accuracy: {gpu_acc:.5f}\n"
        f"Precision: {gpu_precision:.5f}\n"
        f"Recall: {gpu_recall:.5f}\n\n"

    )

    return status_msg, gpu_auc, gpu_acc, top_preds_df, full_preds_df, tgbm_model


# -------------------------
# UI + Gradio
# -------------------------
custom_css = f"""
#header {{
    background-color: {AMD_TEAL};
    color: {TEXT_WHITE};
    padding: 10px;
    border-radius: 10px;
    text-align: center;
    font-size: 1.2em;
    justify-content: space-between;
}}
footer {{visibility: hidden;}}
.gr-button {{
    background-color: {AMD_TEAL} !important;
    color: {AMD_BLACK} !important;
    font-weight: bold;
}}
"""

with gr.Blocks(css=custom_css, title="XGBoost (CPU) vs ThunderGBM (GPU) Benchmark") as demo:
    gr.HTML("<h1>XGBoost CPU vs ThunderGBM GPU — Benchmark</h1>")

    with gr.Row():
        with gr.Column():
            max_depth = gr.Number(value=10, label="Max Depth")
            n_estimators = gr.Number(value=500, label="Number of Trees")
            learning_rate = gr.Number(value=0.15, label="Learning Rate")
            train_btn = gr.Button("Run Benchmark", variant="primary")
            train_output = gr.Textbox(label="Training Status", interactive=False, lines=18)

        with gr.Column():
            auc_box = gr.Number(value=0, label="GPU AUC")
            acc_box = gr.Number(value=0, label="GPU Accuracy")

            gr.Markdown("### Top 20 Predictions (ThunderGBM GPU)")
            top_preds = gr.Dataframe(
                headers=["TransactionID", "Test Fraud Probability", "Fraud Probability"],
                datatype=["str", "number", "number"],
                interactive=False
            )

            download_btn = gr.File(label="Download Full Predictions CSV")

    def run_training(md, ne, lr):
        status, auc, acc, top_df, full_df, model = train_model(md, ne, lr)
        if full_df is not None:
            full_df.to_csv("full_predictions.csv", index=False)
        return status, auc, acc, top_df, "full_predictions.csv", model

    model_state = gr.State()

    train_btn.click(
        fn=run_training,
        inputs=[max_depth, n_estimators, learning_rate],
        outputs=[train_output, auc_box, acc_box, top_preds, download_btn, model_state]
    )

demo.launch(server_name="0.0.0.0")
