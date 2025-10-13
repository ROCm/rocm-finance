import gradio as gr
import pandas as pd
import numpy as np
import lightgbm as lgb
from thundergbm import TGBMClassifier
from sklearn.metrics import roc_auc_score, accuracy_score, precision_score, recall_score
import os
import time
import matplotlib.pyplot as plt

CACHE_PATH = "/root/ieee_preprocessed.pkl"

AMD_TEAL = "#00C2DE"
AMD_BLACK = "#1C1C1C"
TEXT_WHITE = "#FFFFFF"


# ============================================================
# Load & Preprocess
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
# Feature Importance (LightGBM)
# ============================================================
def plot_feature_importance_lgbm(lgb_model, feature_names, top_n=20):
    importance = lgb_model.feature_importances_
    sorted_idx = np.argsort(importance)[::-1][:top_n]

    top_features = np.array(feature_names)[sorted_idx]
    top_importances = importance[sorted_idx]

    plt.figure(figsize=(10, 7))
    plt.barh(top_features[::-1], top_importances[::-1], color=AMD_TEAL)
    plt.title("Top Feature Importances", fontsize=14)
    plt.xlabel("Importance Score", fontsize=12)
    plt.tight_layout()

    return plt


# ============================================================
# CPU vs GPU Training
# ============================================================
def train_model(max_depth, n_estimators, learning_rate):
    df = load_and_preprocess()

    y = df["isFraud"].astype(np.float32)
    X = df.drop(columns=["isFraud"])

    feature_names = list(X.columns)

    split_idx = int(len(df) * 0.8)
    X_train = X.iloc[:split_idx].astype(np.float32).values
    y_train = y.iloc[:split_idx]
    X_test = X.iloc[split_idx:].astype(np.float32).values
    y_test = y.iloc[split_idx:]

    transaction_ids_test = df["TransactionID"].iloc[split_idx:]

    # ============================================================
    # LIGHTGBM CPU
    # ============================================================
    print("\n===== LIGHTGBM CPU TRAINING =====")
    lgb_model = lgb.LGBMClassifier(
        n_estimators=int(n_estimators),
        max_depth=int(max_depth),
        learning_rate=float(learning_rate),
        objective='binary',
        metric='auc',
        boosting_type='gbdt',
        device_type='cpu',
        num_threads=1,
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
    # ThunderGBM GPU
    # ============================================================
    print("\n===== THUNDERGBM GPU TRAINING =====")

    tgbm_model = TGBMClassifier(
        depth=int(max_depth),
        n_trees=int(n_estimators),
        learning_rate=float(learning_rate),
        objective="binary:logistic",
        lambda_tgbm=1.0,
        max_num_bin=128,
        n_parallel_trees=4,
        min_child_weight=4,
        column_sampling_rate=0.8,
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
    # Prediction Table
    # ============================================================
    results_df = pd.DataFrame({
        "TransactionID": transaction_ids_test.values,
        "True Label": y_test.values,
        "Fraud Probability (GPU)": gpu_preds
    }).sort_values(by="True Label", ascending=False)

    top_preds_df = results_df.head(20).reset_index(drop=True)

    # ============================================================
    # Summary (Storytelling)
    # ============================================================
    status_msg = f"""

🎉 <b>Benchmark Complete</b>
<br>
<b>1. CPU Model — LightGBM</b>  
• Time: {cpu_time:.3f} sec  
• AUC: {cpu_auc:.5f}  
• Accuracy: {cpu_acc:.5f}  
• Precision: {cpu_precision:.5f}  
• Recall: {cpu_recall:.5f}  
<br>
<b>2. GPU Model — ThunderGBM</b>  
• Time: {gpu_time:.3f} sec  
• AUC: {gpu_auc:.5f}  
• Accuracy: {gpu_acc:.5f}  
• Precision: {gpu_precision:.5f}  
• Recall: {gpu_recall:.5f}  
<br>
<b>3. GPU Speedup</b>  
⚡ ThunderGBM is <b>{speedup:.2f}× faster</b> than LightGBM on this dataset.
"""

    return (
        status_msg,
        gpu_auc,
        gpu_acc,
        top_preds_df,
        results_df,
        tgbm_model,
        lgb_model,
        feature_names
    )



# ============================================================
# UI Styling
# ============================================================
custom_css = f"""
.info-box {{
    background: #ffffff;
    padding: 18px;
    border-radius: 12px;
    border-left: 6px solid {AMD_TEAL};
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    margin-bottom: 16px;
}}
.title-card {{
    background: linear-gradient(90deg, #00c2de 0%, #0096b3 100%);
    padding: 22px;
    color: white;
    border-radius: 12px;
    font-size: 30px;
    font-weight: 800;
    display:flex;
    justify-content:space-between;
    align-items:center;
}}
"""


# ============================================================
# UI
# ============================================================
with gr.Blocks(css=custom_css, title="ThunderGBM GPU vs LightGBM CPU — Benchmark") as demo:
    
    # Title
    gr.HTML(f"""
    <div style="display:flex; justify-content:space-between; align-items:center; 
                background: linear-gradient(90deg, #00c2de 0%, #0096b3 100%); 
                padding: 22px; border-radius: 12px; color:white;">
        <div style="font-size: 30px; font-weight: 800;">Running ThunderGBM GPU vs LightGBM CPU on IEEE-CIS Fraud Detection</div>
        <img src="https://upload.wikimedia.org/wikipedia/commons/7/7c/AMD_Logo.svg"
             alt="AMD Logo" style="height:55px;">
    </div>
    """
)

    # Dataset Story Section
    gr.HTML("""
    <div class="info-box">
        <h3>Part 1 — The Dataset: IEEE-CIS Fraud Detection</h3>
        <p>
            We begin with a highly complex real-world dataset: the <b>IEEE-CIS Fraud Detection dataset</b>.  
            It combines two large tables:
        </p>
        <ul>
            <li><b>train_transaction.csv</b> — transaction amounts, product codes, card info</li>
            <li><b>train_identity.csv</b> — device, browser, and network metadata</li>
        </ul>
        <p>
            These are merged on <b>TransactionID</b> to build a rich feature space used to determine whether a transaction is fraudulent.
            All categorical values are factorized, and missing values are filled with zero for efficient tree-based learning.
        </p>
    </div>
    """)

    # Model Story Section
    gr.HTML("""
    <div class="info-box">
        <h3>Part 2 — The Models: CPU vs GPU</h3>
        <p>
            The experiment compares two powerful gradient-boosted decision tree engines:
        </p>
        <p>
            <b>LightGBM (CPU)</b><br>
            A highly optimized CPU framework known for fast histogram-based splitting.
            It offers stable and interpretable feature importance.
        </p>
        <p>
            <b>ThunderGBM (GPU)</b><br>
            A GPU-accelerated gradient boosting library leveraging ROCm/CUDA kernels,
            capable of training multiple trees in parallel.
        </p>
        <p>
            The goal: <b>How much faster can GPU boosting be?</b>
        </p>
    </div>
    """)

    # Controls + outputs
    with gr.Row():
        with gr.Column():

            max_depth = gr.Number(value=6, label="Tree Max Depth")
            n_estimators = gr.Number(value=200, label="Number of Trees")
            learning_rate = gr.Number(value=0.05, label="Learning Rate")

            train_btn = gr.Button("🚀 Run Training & Benchmark", variant="primary")
            train_output = gr.HTML(label="Narrative Summary")

            top_preds = gr.Dataframe(
                label="Top Fraud Predictions (What the GPU Model Thinks)",
                headers=["TransactionID", "True Label", "Fraud Probability (GPU)"],
                interactive=False
            )

        with gr.Column():

            auc_box = gr.Number(label="GPU AUC (ThunderGBM)")
            acc_box = gr.Number(label="GPU Accuracy")

            feature_plot = gr.Plot(
                label="How the Model Predicts Fraud?"
            )
            

            download_btn = gr.File(label="Download Full Prediction Results (CSV)")
        # ===========================
    # Output Explanation Block
    # ===========================
    gr.HTML("""
    <div class="info-box">
        <h3>Part 3 — Understanding the Outputs</h3>

        <h4>🔹 AUC (Area Under the ROC Curve)</h4>
        <p>
            AUC measures how well the model can separate fraudulent vs. legitimate transactions.
            A score of <b>1.0</b> is perfect, <b>0.5</b> is random guessing. 
            For fraud detection, values above <b>0.85</b> are considered strong.
        </p>

        <h4>🔹 Accuracy</h4>
        <p>
            Accuracy measures how often the model is correct. However, since fraud is only a tiny portion 
            of all transactions, accuracy can be misleading (predicting all transactions as non-fraud 
            gives high accuracy but zero fraud detection ability).
        </p>

        <h4>🔹 Precision</h4>
        <p>
            Precision answers: <i>"Of all transactions the model flagged as fraud, how many were actually fraud?"</i>
            High precision means fewer false alarms.
        </p>

        <h4>🔹 Recall</h4>
        <p>
            Recall answers: <i>"Of all real fraud cases, how many did the model detect?"</i>
            High recall is crucial because missed fraud means financial losses.
        </p>

        <h4>🔹 Feature Importance Graph</h4>
        <p>
            Shows which features LightGBM relied on most when detecting fraud. 
            Longer bars mean the feature contributed more to the model’s decision-making.
            This helps explain <b>why</b> the model thinks a transaction is suspicious.
        </p>

        <h4>🔹 Top Fraud Predictions Table</h4>
        <p>
            Shows the transactions the ThunderGBM GPU model thought were most likely to be fraudulent. 
            Useful for inspection, validation, and understanding model behavior on real data.
        </p>

        <h4>🔹 Downloadable CSV</h4>
        <p>
            Contains all prediction results — including fraud probabilities for each transaction.
            Ideal for audits, analysis, or feeding into downstream systems.
        </p>
    </div>
    """)

    # Wrapper
    def run_training(md, ne, lr):
        status, auc, acc, top_df, full_df, tgbm_model, lgb_model, feature_names = train_model(md, ne, lr)

        full_df.to_csv("full_predictions.csv", index=False)

        fig = plot_feature_importance_lgbm(lgb_model, feature_names)

        return status, auc, acc, top_df, fig, "full_predictions.csv", tgbm_model

    model_state = gr.State()

    train_btn.click(
        fn=run_training,
        inputs=[max_depth, n_estimators, learning_rate],
        outputs=[
            train_output,
            auc_box,
            acc_box,
            top_preds,
            feature_plot,
            download_btn,
            model_state
        ]
    )

demo.launch(server_name="0.0.0.0")
