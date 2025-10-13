
# **LightGBM ROCm Home Credit Risk Prediction**


This code implements a binary classification model using LightGBM for a Home Credit default risk prediction problem. 


## Data loading and preprocessing
**Kaggle Dataset** -  [Home Credit Default Risk dataset from Kaggle](https://www.kaggle.com/c/home-credit-default-risk/data)  

Loads training data from application_train.csv
Separates features and target: The target variable is TARGET (indicating loan default), and features exclude TARGET and SK_ID_CURR (customer ID)
Handles categorical features: Automatically identifies object-type columns and converts them to categorical data type for LightGBM

### Data splitting
Creates train/validation split: Uses 80% for training, 20% for validation with a fixed random seed (42) for reproducibility

## **Model configuration**

### **LightGBM parameters:**
```
objective: 'binary' - Binary classification task
metric: 'auc' - Uses AUC (Area Under Curve) as evaluation metric
boosting_type: 'gbdt' - Gradient Boosting Decision Trees
learning_rate: 0.05 - Conservative learning rate
num_leaves: 31 - Maximum leaves per tree (controls model complexity)
```
### **Training with early stopping**
**Early stopping**: Stops training if validation metric doesn't improve for 50 rounds
**Logging**: Prints progress every 50 iterations
**Training**: Runs up to 1000 boosting rounds but may stop early

## **Evaluation**
**Prediction**: Uses the best iteration (from early stopping) to make predictions
**Evaluation**: Calculates AUC score on validation set and prints the result

**Final goal** is to predict whether a loan applicant will default on their loan based on their application data.

### **Install LightGBM**
Install ROCm first. The easiest way is to get the official docker images from docker hub which have ROCm installed.

-   For ROCm 7.0    
	 ```bash
	 docker run --cap-add=SYS_PTRACE --ipc=host --privileged=true --shm-size=128GB --network=host --device=/dev/kfd --device=/dev/dri --group-add video -it -v $HOME:$HOME --name rocm7 rocm/dev-ubuntu-24.04:7.0.2-complete
	 ```
-   For ROCm 6.4
	   ```bash
	   docker run --cap-add=SYS_PTRACE --ipc=host --privileged=true --shm-size=128GB --n
	   ```
-   Install LightGBM from the AMD hosted PYPI repoitory.
    
	```bash
	pip install lightgbm --index-url=http://pypi.amd.com/simple
	```
-  Verification

	```bash
	pip show -v lightgbm 
	Name: lightgbm Version: 4.6.0.99 
	Summary: LightGBM Python-package Home-page: https://github.com/microsoft/LightGBM 
	Author: Author-email: License: The MIT License (MIT)
	...(Truncated)
	```	
**Run the python script:**
```bash
python lightgbm_example.py 
```
**Example Output:**
```
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
<img width="1327" height="1251" alt="image" src="https://github.com/user-attachments/assets/49e421a4-7c64-4f59-b216-c4d90dbf6f39" />

