import gradio as gr
import pandas as pd
import numpy as np
import xgboost as xgb
import lightgbm as lgb
from thundergbm import TGBMClassifier
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score
import os
import time

CACHE_PATH = "/root/ieee_preprocessed.pkl"

AMD_TEAL = "#00C2DE"
AMD_BLACK = "#1C1C1C"
TEXT_WHITE = "#FFFFFF"


# ============================================================
# Load & preprocess
# ============================================================
def load_and_preprocess():
    if os.path.exists(CACHE_PATH):
        print("Loading cached preprocessed dataset…")
        return pd.read_pickle(CACHE_PATH)

    trans_path = "/root/train_transaction.csv"
    ident_path = "/root/train_identity.csv"

    if not os.path.exists(trans_path) or not os.path.exists(ident_path):
        raise FileNotFoundError("Missing IEEE-CIS dataset CSVs.")

    print("Loading transaction data…")
    train_transaction = pd.read_csv(trans_path, low_memory=False)

    print("Loading identity data…")
    train_identity = pd.read_csv(ident_path, low_memory=False)

    print("Merging datasets…")
    df = train_transaction.merge(train_identity, on="TransactionID", how="left")

    print("Encoding categorical features…")
    for col in df.select_dtypes(include=["object", "category"]):
        df[col], _ = pd.factorize(df[col], sort=False)

    df = df.fillna(0).astype(np.float32)

    print("Saving cached preprocessed dataset…")
    df.to_pickle(CACHE_PATH)
    return df


# ============================================================
# CPU vs GPU Training
# ============================================================
def train_model(max_depth, n_estimators, learning_rate):
    df = load_and_preprocess()

    y = df["isFraud"].astype(np.float32)
    X = df.drop(columns=["isFraud"])

    split_idx = int(len(df) * 0.8)
    X_train = X.iloc[:split_idx].astype(np.float32).values
    y_train = y.iloc[:split_idx]
    X_test = X.iloc[split_idx:].astype(np.float32).values
    y_test = y.iloc[split_idx:]

    transaction_ids_test = df["TransactionID"].iloc[split_idx:]

    # ============================================================
    # XGBOOST CPU
    # ============================================================
# ============================================================
# CPU (LIGHTGBM)
# ============================================================
    print("\n===== LIGHTGBM CPU TRAINING =====")
    lgb_model = lgb.LGBMClassifier(
        n_estimators=int(n_estimators),
        max_depth=int(max_depth),
        learning_rate=float(learning_rate),
        objective= 'binary',
        metric= 'auc',
        boosting_type= 'gbdt',
        device_type='cpu',
        num_threads= 1,
        n_jobs=1
    )

    cpu_start = time.time()
    lgb_model.fit(X_train, y_train)
    cpu_time = time.time() - cpu_start

    lgb_probs = lgb_model.predict_proba(X_test)[:, 1]
    lgb_labels = (lgb_probs > 0.5).astype(int)

    cpu_auc = roc_auc_score(y_test, lgb_probs)
    cpu_acc = accuracy_score(y_test, lgb_labels)
    cpu_precision = precision_score(y_test, lgb_labels)
    cpu_recall = recall_score(y_test, lgb_labels)


    # ============================================================
    # THUNDERGBM GPU — Optimized for ROCm speed
    # ============================================================
    print("\n===== THUNDERGBM GPU TRAINING =====")

    tgbm_model = TGBMClassifier(
        depth=int(max_depth),
        n_trees=int(n_estimators),
        learning_rate=float(learning_rate),

        objective="binary:logistic",
        lambda_tgbm=1.0,

        # GPU-optimal settings
        max_num_bin=128,            # more parallel histogram work
        n_parallel_trees=4,         # increase GPU thread blocks
        min_child_weight=4,
        column_sampling_rate=0.8,   # avoid sampling overhead
        verbose=0,
        n_gpus=1
    )

    gpu_start = time.time()
    tgbm_model.fit(X_train, y_train)
    gpu_time = time.time() - gpu_start

    gpu_preds = tgbm_model.predict(X_test)

    gpu_auc = roc_auc_score(y_test, gpu_preds)
    gpu_acc = accuracy_score(y_test, gpu_preds)
    gpu_precision = precision_score(y_test, gpu_preds)
    gpu_recall = recall_score(y_test, gpu_preds)

    speedup = cpu_time / gpu_time if gpu_time > 0 else 0

    # ============================================================
    # Prediction Table (GPU)
    # ===========================================================

    results_df = pd.DataFrame({
        "TransactionID": transaction_ids_test.values,
        "Test Fraud Probability": y_test.values,
        "Fraud Probability": gpu_preds
    }).sort_values(by="Test Fraud Probability", ascending=False)  # sorted descending (1 → 0)

    top_preds_df = results_df.head(20).reset_index(drop=True)
    full_preds_df = results_df

    # ============================================================
    # Output summary
    # ============================================================
    status_msg = f"""
====== CPU vs GPU Benchmark Complete ======

=== LIGHTGBM CPU ===
Runtime: {cpu_time:.3f} sec
AUC:      {cpu_auc:.5f}
Accuracy: {cpu_acc:.5f}
Precision:{cpu_precision:.5f}
Recall:   {cpu_recall:.5f}

=== THUNDERGBM GPU ===
Runtime: {gpu_time:.3f} sec
AUC:      {gpu_auc:.5f}
Accuracy: {gpu_acc:.5f}
Precision:{gpu_precision:.5f}
Recall:   {gpu_recall:.5f}

=== GPU SPEEDUP ===
ThunderGBM GPU is {speedup:.2f}× faster than LightGBM CPU.
"""

    return status_msg, gpu_auc, gpu_acc, top_preds_df, full_preds_df, tgbm_model


# ============================================================
# UI
# ============================================================
custom_css = f"""
#header {{
    background-color: {AMD_TEAL};
    color: {TEXT_WHITE};
    padding: 10px;
    border-radius: 10px;
    text-align: center;
    font-size: 1.2em;
    font-weight: bold;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}
#header img {{
    height: 40px;
}}
footer {{visibility: hidden;}}
.gr-button {{
    background-color: {AMD_TEAL} !important;
    color: {AMD_BLACK} !important;
    font-weight: bold;
}}
"""

with gr.Blocks(css=custom_css, title="LightGBM CPU vs ThunderGBM GPU — Benchmark") as demo:
    gr.HTML(f"""
    <div style="position: relative; padding: 20px; background: linear-gradient(135deg, #f8f9fa 0%, #00c2de 100%); border-radius: 10px; margin-bottom: 20px;">
        <h1 style="margin:0; font-weight: 700;">LightGBM CPU vs ThunderGBM GPU — Benchmark</h1>
        <img src="https://upload.wikimedia.org/wikipedia/commons/7/7c/AMD_Logo.svg"
             alt="AMD Logo" style="position: absolute; top: 10px; right: 20px; height: 50px;">
    </div>
    """)

    with gr.Row():
        with gr.Column():
            max_depth = gr.Number(value=6, label="Max Depth")
            n_estimators = gr.Number(value=200, label="Number of Trees")
            learning_rate = gr.Number(value=0.05, label="Learning Rate")

            train_btn = gr.Button("Run Benchmark", variant="primary")
            train_output = gr.Textbox(label="Training Status", lines=18)

        with gr.Column():
            auc_box = gr.Number(label="GPU AUC")
            acc_box = gr.Number(label="GPU Accuracy")
            top_preds = gr.Dataframe(headers=["TransactionID", "Test Fraud Probability", "Fraud Probability"])
            download_btn = gr.File()

    def run_training(md, ne, lr):
        status, auc, acc, top_df, full_df, model = train_model(md, ne, lr)
        full_df.to_csv("full_predictions.csv", index=False)
        return status, auc, acc, top_df, "full_predictions.csv", model

    model_state = gr.State()

    train_btn.click(
        fn=run_training,
        inputs=[max_depth, n_estimators, learning_rate],
        outputs=[train_output, auc_box, acc_box, top_preds, download_btn, model_state]
    )

demo.launch(server_name="0.0.0.0")
