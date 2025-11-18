# ROCm ThunderGBM Credit Card Fraud Detection (IEEE-CIS Dataset Demo)

**High-performance Fraud Detection with AMD ROCm and ThunderGBM**

This project demonstrates an interactive **Gradio app** that trains and tests a **ThunderGBM model** on the IEEE-CIS credit card fraud dataset. 
It leverages **AMD ROCm GPUs** for acceleration, supports feature preprocessing, and provides top predicted fraud transactions with full CSV export.

## Features

- Train **ThunderGBM** on ROCm-enabled AMD GPUs  
- Automatic preprocessing of **transaction + identity datasets**  
- 80/20 train/test split  
- Metrics: ROC-AUC, Accuracy, Precision, Recall  
- Top 20 predicted fraud transactions  
- Download full predictions CSV  
- AMD-themed **Gradio UI**  

## Requirements

- Python 3.8+  
- ROCm-enabled AMD GPU (recommended for ThunderGBM acceleration)  
- Key Python packages:

```bash
pip install numpy pandas scipy scikit-learn gradio
```

## Installing ThunderGBM with ROCm

Install ROCm following AMD instructions:
ROCm Installation Guide

Install ThunderGBM prebuilt ROCm wheel:
```bash
# Example: adapt version numbers to your Python version
pip install thundergbm-0.3.16-py3-none-any.whl
```

Verify installation:
```bash
import thundergbm
print(thundergbm.__version__)
```

Ensure your AMD GPU is detected. ThunderGBM will automatically use GPU if n_gpus=1.

## Dataset

1. IEEE-CIS Fraud Detection:
Kaggle dataset

2. Requires two CSV files in /root/ (or adjust paths in code):

/root/train_transaction.csv
/root/train_identity.csv

3. TransactionID is required for merging; isFraud is the target label

4. Preprocessing caches to /root/ieee_preprocessed.pkl for faster reloads

## Usage

Launch the app:
```bash
python app.py
```

Open the interface in your browser at http://0.0.0.0:7860 (default port)

## Configure training options:

1. Max depth of trees

2. Number of trees (estimators)

3. Learning rate

4. Click "Train & Predict"

## View results:

1. Test ROC-AUC and Accuracy metrics

2. Top 20 predicted fraud transactions

3. Download full prediction CSV

## Example Output

Training Status Example:

Training complete!
Test ROC-AUC = 0.94512
Test Accuracy = 0.98734
Test Precision = 0.87456
Test Recall = 0.90123

<img width="1369" height="768" alt="Screenshot 2025-11-18 105541" src="https://github.com/user-attachments/assets/f65a8f1e-3fdd-406c-bbe2-eacdafef7067" />


Top 20 Predictions:

TransactionID	Test Fraud Probability	Fraud Probability
100001	                  1	                    1
100023	                  0	                    0

File Structure
.
├── app.py                       # Main Gradio app
├── train_transaction.csv         # Dataset
├── train_identity.csv            # Dataset
├── ieee_preprocessed.pkl         # Cached preprocessed dataset
├── full_predictions.csv          # Generated predictions CSV
├── README.md                     # Documentation

## Customization

1. Modify AMD theme colors in custom_css

2. Adjust ThunderGBM hyperparameters: max_depth, n_estimators, learning_rate

3. Cache location can be changed by editing CACHE_PATH

## License

MIT License – free to use and modify.

## Acknowledgements

ThunderGBM
 – GPU-accelerated gradient boosting

Gradio
 – Interactive web UI

IEEE-CIS Fraud Detection Dataset

AMD ROCm
 – GPU acceleration platform
