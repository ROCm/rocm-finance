import argparse
import time
import ml_dataset_loader.datasets as data_loader
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_squared_error, accuracy_score

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--rows', type=int, default=None,
                        help='Max rows to benchmark for each dataset.')
    parser.add_argument('--num_rounds', type=int, default=500, help='Boosting rounds.')
    args = parser.parse_args()

    X,y = data_loader.get_airline(num_rows = args.rows)

    dtrain = xgb.DMatrix(X, y)

    times = []
    # XGBoost 2.x / 3.x: no n_gpus; pick one device per iter (cuda:0 .. cuda:7).
    for gpu_id in range(8):
        print("Running XGBoost on cuda:{} ...".format(gpu_id))
        params = {
            'objective': 'binary:logistic',
            'tree_method': 'hist',
            'device': 'cuda:{}'.format(gpu_id),
        }
        start = time.time()
        bst = xgb.train(params, dtrain, args.num_rounds)
        times.append(time.time() - start)
        del bst

    print(times)

if __name__ == "__main__":
    main()
