# ROCm ThunderGBM vs LightGBM Benchmark — Credit Card Fraud Detection (IEEE-CIS Dataset)

This project benchmarks **ThunderGBM** (GPU-accelerated with AMD ROCm) against **LightGBM** (CPU) using the IEEE-CIS credit card fraud detection dataset.

It demonstrates the performance gains of GPU training and compares model accuracy metrics through an interactive **Gradio app**.

---

## Features

- Train **ThunderGBM** on ROCm-enabled AMD GPUs  
- Train **LightGBM** on CPU for baseline comparison  
- Preprocessing of merged transaction + identity datasets  
- 80/20 chronological train/test split  
- Evaluate metrics: ROC-AUC, Accuracy, Precision, Recall  
- Visualize top 20 fraud predictions  
- Download full prediction CSV  
- AMD-themed Gradio UI with feature importance plots  

---

## Requirements

- Python 3.8 or higher  
- ROCm-enabled AMD GPU (required for ThunderGBM GPU acceleration)  

## Installing ROCm, ThunderGBM, and LightGBM

**Step 1: Install ROCm**

Use official Docker images for ROCm setup.

 ```bash
ROCm 7.0

docker run --cap-add=SYS_PTRACE --ipc=host --privileged=true --shm-size=128GB --network=host \
  --device=/dev/kfd --device=/dev/dri --group-add video -it -v $HOME:$HOME \
  --name rocm7 rocm/dev-ubuntu-24.04:7.0.2-complete
```
 ```bash
ROCm 6.4

docker run --cap-add=SYS_PTRACE --ipc=host --privileged=true --shm-size=128GB --network=host \
  --device=/dev/kfd --device=/dev/dri --group-add video -it -v $HOME:$HOME \
  --name rocm6 rocm/dev-ubuntu-24.04:6.4.4-complete
```
**Step 2: Install ThunderGBM**

Inside the ROCm environment, install ThunderGBM prebuilt wheel:
 ```bash
pip install amd_thundergbm --extra-index-url=https://pypi.amd.com/rocm-7.0.2/simple/
```

**Verify**:
 ```bash
import thundergbm
print(thundergbm.__version__)
```

**Step 3: Install LightGBM with ROCm support**

Install LightGBM from AMD PyPI repository:
 ```bash
pip install amd_lightgbm --extra-index-url=https://pypi.amd.com/rocm-7.0.2/simple/
```

**Verify**:
 ```bash
pip show -v lightgbm
```
```bash
Expected output snippet:

Name: lightgbm
Version: 4.6.0.99
Summary: LightGBM Python-package
Home-page: https://github.com/microsoft/LightGBM
License: The MIT License (MIT)
```
**Step 4: Install the other python packages**

```bash
pip install numpy pandas scipy scikit-learn lightgbm thundergbm gradio matplotlib
```


## Dataset
IEEE-CIS Fraud Detection dataset (available on Kaggle) - Head over to https://www.kaggle.com/c/ieee-fraud-detection
to sign up and grab the train_transaction and train_identity dataset.

Place the following CSV files under /root/ or adjust paths accordingly:

/root/train_transaction.csv  
/root/train_identity.csv


Data merges on TransactionID; target label is isFraud

Preprocessing cache saved at /root/ieee_preprocessed.pkl for faster reloads

## Usage

Run the benchmark app:
```bash
python thundergbm_lightgbm.py
```

Open your browser at:
```bash
http://0.0.0.0:7860
```

Configure training parameters (max depth, number of trees, learning rate) and click Train & Predict.
```bash
Example Benchmark Output
====== LIGHTGBM CPU RESULTS ======
CPU Training Time: 17.641 sec
AUC: 0.89350
Accuracy: 0.97356
Precision: 0.77595
Recall: 0.32554

====== THUNDERGBM GPU RESULTS ======
GPU Training Time: 12.150 sec
AUC: 0.72883
Accuracy: 0.94627
Precision: 0.31912
Recall: 0.49532

====== GPU SPEEDUP ======
ThunderGBM is 1.45× faster than LightGBM on this dataset.
```

<img width="1336" height="1148" alt="image" src="https://github.com/user-attachments/assets/de8c9db8-6896-4c17-ac4d-da768ddb9cbb" />
<img width="1345" height="424" alt="image" src="https://github.com/user-attachments/assets/6d2ba09d-0613-47df-876e-1acf1ce64652" />

## Output Files

full_predictions.csv — full fraud probability predictions using ThunderGBM GPU model

## Integration & Customization

1. Modify AMD-themed colors via the Gradio custom_css variable

2. Adjust hyperparameters (max_depth, n_estimators, learning_rate) in the UI
   
**max_depth** - Maximum depth of each decision tree in the ensemble. Controls how “deep” or complex each tree can grow.

**n_estimators** - Number of trees in the boosting ensemble. Determines how many sequential trees are built.

**learning_rate** - Shrinks the contribution of each tree when added to the ensemble. 
Lower learning_rate → each tree contributes less → slower learning → may require more trees (n_estimators).
Higher learning_rate → faster learning → risk of overfitting.

4. Change dataset/cache paths by editing CACHE_PATH in the script

## License

MIT License – free to use and modify.

## Acknowledgements

1. ThunderGBM — GPU-accelerated gradient boosting library (https://github.com/ROCmSoftwarePlatform/thundergbm
)

2. LightGBM — High-performance gradient boosting framework (https://github.com/microsoft/LightGBM
)

3. Gradio — Interactive UI toolkit (https://gradio.app
)

4. IEEE-CIS Fraud Detection Dataset — Kaggle competition (https://www.kaggle.com/c/ieee-fraud-detection
)

5. AMD ROCm — GPU acceleration platform (https://rocmdocs.amd.com/en/latest/
)
