import gradio as gr
import pandas as pd
import numpy as np
from thundergbm import TGBMClassifier
from scipy import sparse
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score
import os
import time  # 

CACHE_PATH = "./ieee_preprocessed.pkl"

# -------------------------
# AMD UI colors
# -------------------------
AMD_TEAL = "#00C2DE"
AMD_BLACK = "#1C1C1C"
TEXT_WHITE = "#FFFFFF"

def load_and_preprocess():
    if os.path.exists(CACHE_PATH):
        print("Loading cached preprocessed dataset…")
        return pd.read_pickle(CACHE_PATH)

    trans_path = "./train_transaction.csv"
    ident_path = "./train_identity.csv"

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


def train_model(max_depth, n_estimators, learning_rate):
    try:
        df = load_and_preprocess()
    except Exception as e:
        return str(e), 0, 0, None, None, None, 0  # ADD GPU TIME

    if "isFraud" not in df.columns:
        return "ERROR: 'isFraud' not found.", 0, 0, None, None, None, 0  # ADD GPU TIME

    y = df["isFraud"]
    X = df.drop(columns=["isFraud"])

    split_idx = int(len(df) * 0.8)
    X_train = X.iloc[:split_idx]
    y_train = y.iloc[:split_idx]
    X_test = X.iloc[split_idx:]
    y_test = y.iloc[split_idx:]

    X_train = sparse.csr_matrix(X_train.values)
    X_test = sparse.csr_matrix(X_test.values)
    transaction_ids_test = df["TransactionID"].iloc[split_idx:]
    model = TGBMClassifier(
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

    print("Training ThunderGBM…")
    start_gpu = time.time()                # <-- ADD THIS
    model.fit(X_train, y_train)
    gpu_time = time.time() - start_gpu     # <-- ADD THIS

    print(f"ThunderGBM GPU training time: {gpu_time:.2f} seconds")  # You can print or report this
    print("Predicting…")
    preds = model.predict(X_test)

    auc = roc_auc_score(y_test, preds)
    acc = accuracy_score(y_test, preds)
    precision_s = precision_score(y_test, preds)
    recall_s = recall_score(y_test, preds)

    train_preds = model.predict(X_train)

    train_auc = roc_auc_score(y_train, train_preds)
    train_acc = accuracy_score(y_train, train_preds)
    train_precision = precision_score(y_train, train_preds)
    train_recall = recall_score(y_train, train_preds)

    print(f"Train ROC-AUC: {train_auc:.5f}, Accuracy: {train_acc:.5f}, Precision: {train_precision:.5f}, Recall: {train_recall:.5f}")
    print(f"Test ROC-AUC: {auc:.5f}, Accuracy: {acc:.5f}, Precision: {precision_s:.5f}, Recall: {recall_s:.5f}")

    results_df = pd.DataFrame({
        "TransactionID": transaction_ids_test.values,
        "Test Fraud Probability": y_test.values,
        "Fraud Probability": preds
    }).sort_values(by="Test Fraud Probability", ascending=False)  # sorted descending (1 → 0)

    top_preds_df = results_df.head(20).reset_index(drop=True)
    full_preds_df = results_df.reset_index(drop=True)

    return (
        f"Training complete!\nTest ROC-AUC = {auc:.5f}\nTest Accuracy = {acc:.5f}\n"
        f"Test Precision = {precision_s:.5f}\nTest Recall = {recall_s:.5f}\n"
        f"ThunderGBM GPU training time: {gpu_time:.2f} seconds",  # <-- SHOW GPU TIME
        auc,
        acc,
        top_preds_df,
        full_preds_df,
        model,
        gpu_time                 # <-- RETURN GPU TIME
    )

def predict_on_test(model):
    if model is None:
        return "ERROR: Train a model first."
    return "Model ready."

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

with gr.Blocks(css=custom_css, title="ROCm ThunderGBM Fraud Detection") as demo:
    gr.HTML(f"""
    <div style="position: relative; padding: 20px; background: linear-gradient(135deg, #f8f9fa 0%, #00c2de 100%); border-radius: 10px; margin-bottom: 20px;">
        <h1 style="margin:0; font-weight: 700;">ThunderGBM Fraud Detection — Optimized IEEE-CIS Demo</h1>
        <img src="https://upload.wikimedia.org/wikipedia/commons/7/7c/AMD_Logo.svg"
             alt="AMD Logo" style="position: absolute; top: 10px; right: 20px; height: 50px;">
    </div>
    """)

    with gr.Row():

        with gr.Column(scale=1):
            max_depth = gr.Number(value=10, label="Max Depth")
            n_estimators = gr.Number(value=500, label="Number of Trees")
            learning_rate = gr.Number(value=0.15, label="Learning Rate")
            train_btn = gr.Button("Train & Predict", variant="primary")
            train_output = gr.Textbox(label="Training Status", interactive=False, lines=8)  # <-- Make it a bit taller
            gpu_time_box = gr.Number(value=0, label="ThunderGBM GPU Training Time (sec)")   # <-- ADD BOX

        with gr.Column(scale=1):
            auc_box = gr.Number(value=0, label="Test ROC-AUC")
            acc_box = gr.Number(value=0, label="Test Accuracy")

            gr.Markdown("### Top 20 Predictions (Fraud Probability)")
            top_preds = gr.Dataframe(headers=["TransactionID", "Test Fraud Probability", "Fraud Probability"], datatype=["str", "number", "number"], interactive=False)

            download_btn = gr.File(label="Download Full Predictions CSV")

    def run_training(md, ne, lr):
        status, auc, acc, top_df, full_df, model, gpu_time = train_model(md, ne, lr)
        if full_df is not None:
            full_df.to_csv("full_predictions.csv", index=False)
        else:
            full_df = pd.DataFrame()
        return status, auc, acc, top_df, ("full_predictions.csv" if not full_df.empty else None), model, gpu_time

    model_state = gr.State()

    train_btn.click(
        fn=run_training,
        inputs=[max_depth, n_estimators, learning_rate],
        outputs=[train_output, auc_box, acc_box, top_preds, download_btn, model_state, gpu_time_box]  # <-- INCLUDE GPU TIME
    )

demo.launch(server_name="0.0.0.0", share=True)
