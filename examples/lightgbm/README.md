# LightGBM ROCm — Home Credit Default Risk Prediction

This repository demonstrates a **binary classification model** using **LightGBM** to predict loan default risk for the Home Credit Default Risk dataset. The model leverages **LightGBM’s GPU/CPU capabilities** via AMD ROCm for accelerated training.

---

## Dataset

**Kaggle Dataset:** [Home Credit Default Risk](https://www.kaggle.com/c/home-credit-default-risk/data)  - Head over to this Kaggle website and sign up!

- **Training file:** `application_train.csv`  
- **Target variable:** `TARGET` (1 = default, 0 = no default)  
- **Exclusions:** `SK_ID_CURR` (customer ID) is excluded from features.  
- **Categorical features:** Object-type columns are automatically converted to categorical type for LightGBM.  

---

## Data Preprocessing

- Loads the dataset and separates **features** and **target**  
- Handles missing values and factorizes categorical columns  
- **Train/Validation split:** 80% training, 20% validation  
- **Random seed:** 42 (ensures reproducibility)  

---

## Model Configuration

**LightGBM Parameters:**

| Parameter       | Value | Description |
|-----------------|-------|-------------|
| `objective`     | `'binary'` | Binary classification task |
| `metric`        | `'auc'`    | Evaluation metric: Area Under Curve |
| `boosting_type` | `'gbdt'`   | Gradient Boosted Decision Trees |
| `learning_rate` | 0.05       | Conservative learning rate for stable training |
| `num_leaves`    | 31         | Maximum leaves per tree (controls model complexity) |

**Training Settings:**

- **Early Stopping:** Stops if validation metric does not improve for 50 rounds  
- **Logging:** Displays progress every 50 iterations  
- **Boosting Rounds:** Up to 1000, may stop early based on validation  

---

## Evaluation

- Predictions are made using the **best iteration** determined by early stopping  
- Evaluates **AUC (Area Under the ROC Curve)** on the validation set  
- Provides a performance summary for model accuracy and discrimination ability  

**Goal:** Predict whether a loan applicant will default on their loan based on their application features.

---

## Installation

### Step 1: Install ROCm

Run the official ROCm Docker image for your GPU environment:

- **ROCm 7.0**
```bash
docker run --cap-add=SYS_PTRACE --ipc=host --privileged=true --shm-size=128GB \
```

- **ROCm 6.4**
```bash
docker run --cap-add=SYS_PTRACE --ipc=host --privileged=true --shm-size=128GB \
  --network=host --device=/dev/kfd --device=/dev/dri --group-add video \
  -it -v $HOME:$HOME --name rocm6 rocm/dev-ubuntu-24.04:6.4.4-complete
```

### Step 2: Install LightGBM

Install the ROCm-compatible LightGBM package:
```bash
pip install amd_lightgbm --extra-index-url=https://pypi.amd.com/rocm-7.0.2/simple/
```

**Verify Installation:**

```bash
pip show -v lightgbm
```

Expected output:

Name: lightgbm
Version: 4.6.0.99
Summary: LightGBM Python-package
Home-page: https://github.com/microsoft/LightGBM
License: The MIT License (MIT)

### Step 3: Running the Script

```bash
python lightgbm_example.py
```

```bash
Example Output:

Training until validation scores don't improve for 50 rounds
[50]    valid_0's auc: 0.747234
[100]   valid_0's auc: 0.755118
[150]   valid_0's auc: 0.757008
[200]   valid_0's auc: 0.757516
[250]   valid_0's auc: 0.757721
Early stopping, best iteration is:
[232]   valid_0's auc: 0.757778
Validation AUC: 0.7578
```

## Example Output

<img width="1008" height="965" alt="image" src="https://github.com/user-attachments/assets/7c5bf6a8-b38c-4176-844e-986111ef9109" />

## File Structure
.
├── lightgbm.py        # Main script for training and evaluation
├── application_train.csv       # Kaggle training dataset
├── README.md                   # Documentation

## Customization

1. Adjust LightGBM hyperparameters: learning_rate, num_leaves, max_depth

**learning_rate** - Shrinks the contribution of each tree when added to the ensemble. 

Lower learning_rate → each tree contributes less → slower learning → may require more trees (n_estimators). 

Higher learning_rate → faster learning → risk of overfitting.

**max_leaves** - Maximum number of leaves (terminal nodes) per tree. More leaves → tree can capture more complex pattern

**max_depth** - Maximum depth of each decision tree in the ensemble. Controls how “deep” or complex each tree can grow

2. Modify train/validation split ratio in the script

## License

MIT License — free to use and modify.

## References

1. Home Credit Default Risk Dataset - https://www.kaggle.com/c/home-credit-default-risk

2. AMD ROCm Documentation






















  --network=host --device=/dev/kfd --device=/dev/dri --group-add video \
  -it -v $HOME:$HOME --name rocm7 rocm/dev-ubuntu-24.04:7.0.2-complete
