import argparse
import itertools
import os
import sys
import time

sys.path.insert(0, 'catboost/catboost/python-package')
import ml_dataset_loader.datasets as data_loader
import numpy as np
import pandas as pd

# Optional GBM framework imports
try:
    import xgboost as xgb
except ImportError:
    xgb = None

try:
    import lightgbm as lgb
except ImportError:
    lgb = None

try:
    import catboost as cat
except ImportError:
    cat = None

from sklearn.metrics import (
    accuracy_score,
    mean_squared_error,
    ndcg_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Global parameters
random_seed = 0
max_depth = 6
learning_rate = 0.1
min_split_loss = 0
min_weight = 1
l1_reg = 0
l2_reg = 1


def _groups_from_qid(qid):
    return [len(list(g)) for _, g in itertools.groupby(qid)]


def _mean_ndcg_at_10(y_true, y_pred, qid):
    vals = []
    i, n = 0, len(qid)
    while i < n:
        j = i + 1
        while j < n and qid[j] == qid[i]:
            j += 1
        yt = y_true[i:j].astype(float).reshape(1, -1)
        yp = y_pred[i:j].astype(float).reshape(1, -1)
        k = min(10, yt.shape[1])
        if yt.shape[1] >= 2:
            vals.append(ndcg_score(yt, yp, k=k))
        i = j
    return float(np.mean(vals)) if vals else 0.0


def _tree_max_depth(data):
    return data.bm_max_depth if data.bm_max_depth is not None else max_depth


class Data:
    def __init__(
        self,
        X,
        y,
        name,
        task,
        metric,
        train_size=0.6,
        validation_size=0.2,
        test_size=0.2,
        bm_max_depth=None,
        bm_eval_metric=None,
    ):
        assert (train_size + validation_size + test_size) == 1.0
        self.name = name
        self.task = task
        self.metric = metric
        self.bm_max_depth = bm_max_depth
        self.bm_eval_metric = bm_eval_metric
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_seed
        )

        self.X_train, self.X_val, self.y_train, self.y_val = train_test_split(
            self.X_train,
            self.y_train,
            test_size=validation_size / (1 - test_size),
            random_state=random_seed,
        )

        assert (
            self.X_train.shape[0] + self.X_val.shape[0] + self.X_test.shape[0]
        ) == X.shape[0]

        # Multiclass: XGBoost/LightGBM expect labels in [0, num_class) and num_class == #classes.
        # Using only max(y_test)+1 breaks when a stratified split is not used and the test fold
        # misses the largest original label (GPU hist can then diverge; CPU may appear OK).
        self.num_classes = None
        if task == "Multiclass classification":
            le = LabelEncoder()
            self.y_train = le.fit_transform(np.asarray(self.y_train).ravel())
            self.y_val = le.transform(np.asarray(self.y_val).ravel())
            self.y_test = le.transform(np.asarray(self.y_test).ravel())
            self.num_classes = int(len(le.classes_))


class RankingData:
    """Learning-to-rank data: split by query id (PeerJ YLTR / MQ2008 style)."""

    def __init__(
        self,
        X,
        y,
        qid,
        name,
        metric,
        train_q=0.6,
        val_q=0.2,
        test_q=0.2,
        bm_max_depth=None,
        bm_eval_metric=None,
    ):
        assert abs(train_q + val_q + test_q - 1.0) < 1e-6
        self.name = name
        self.task = "Learning to rank"
        self.metric = metric
        self.bm_max_depth = bm_max_depth
        self.bm_eval_metric = bm_eval_metric
        unique_q = np.unique(qid)
        rng = np.random.RandomState(random_seed)
        rng.shuffle(unique_q)
        nq = len(unique_q)
        n_test = max(1, int(nq * test_q))
        n_val = max(1, int(nq * val_q))
        n_train = nq - n_val - n_test
        if n_train < 1:
            n_train = 1
            n_val = max(1, (nq - n_train) // 2)
            n_test = nq - n_train - n_val
        q_train = set(unique_q[:n_train])
        q_val = set(unique_q[n_train : n_train + n_val])
        q_test = set(unique_q[n_train + n_val :])

        def take(mask):
            return X[mask], y[mask], qid[mask]

        m_tr = np.isin(qid, list(q_train))
        m_va = np.isin(qid, list(q_val))
        m_te = np.isin(qid, list(q_test))
        self.X_train, self.y_train, self.qid_train = take(m_tr)
        self.X_val, self.y_val, self.qid_val = take(m_va)
        self.X_test, self.y_test, self.qid_test = take(m_te)


def eval(data, pred):
    if data.metric == "RMSE":
        return np.sqrt(mean_squared_error(data.y_test, pred))
    elif data.metric == "Accuracy":
        # Threshold prediction if binary classification
        if data.task == "Classification":
            pred = pred > 0.5
        elif data.task == "Multiclass classification":
            if pred.ndim > 1:
                pred = np.argmax(pred, axis=1)
        return accuracy_score(data.y_test, pred)
    elif data.metric == "AUC":
        return float(roc_auc_score(data.y_test, pred))
    elif data.metric == "NDCG@10":
        return _mean_ndcg_at_10(data.y_test, pred, data.qid_test)
    else:
        raise ValueError("Unknown metric: " + data.metric)


def _ensure_multiindex_columns(df):
    """
    Tuple labels must be a real MultiIndex. With a flat Index of tuples, pandas treats
    df.loc[row, (a, b)] as nested keys and writes to separate columns a, b — leaving the
    tuple columns NaN (see pandas loc with tuple on non-MultiIndex columns).
    """
    if isinstance(df.columns, pd.MultiIndex):
        return
    if len(df.columns) == 0:
        # from_tuples([]) raises on modern pandas; two empty level arrays = 0 columns, 2 levels
        df.columns = pd.MultiIndex.from_arrays([[], []])
        return
    tuples = []
    for c in df.columns:
        if isinstance(c, tuple) and len(c) == 2:
            tuples.append(c)
        else:
            tuples.append((str(c), ""))
    df.columns = pd.MultiIndex.from_tuples(tuples)


def add_data(df, algorithm, data, elapsed, metric):
    time_col = (data.name, 'Time(s)')
    metric_col = (data.name, data.metric)
    _ensure_multiindex_columns(df)
    for col in (time_col, metric_col):
        if col not in df.columns:
            df[col] = np.nan
    df.loc[algorithm, time_col] = elapsed
    df.loc[algorithm, metric_col] = metric


def configure_xgboost(data, use_gpu, args, tree_method="hist"):
    # XGBoost 2.x / 3.x: hist or approx + device (ROCm GPU builds still use device="cuda" / "cuda:N").
    params = {
        'max_depth': _tree_max_depth(data),
        'learning_rate': learning_rate,
        'gamma': min_split_loss,
        'min_child_weight': min_weight,
        'alpha': l1_reg,
        'lambda': l2_reg,
        'tree_method': tree_method,
        'verbosity': args.debug_verbose,
    }
    if use_gpu:
        # XGBoost 3.x: use default GPU (set CUDA_VISIBLE_DEVICES to pick a card).
        # Legacy --n_gpus counted GPUs for old gpu_hist; multi-GPU training is not mapped here.
        params['device'] = 'cuda'
    else:
        params['device'] = 'cpu'

    if data.task == "Regression":
        params["objective"] = "reg:squarederror"
    elif data.task == "Multiclass classification":
        params["objective"] = "multi:softmax"
        params["num_class"] = data.num_classes
    elif data.task == "Classification":
        params["objective"] = "binary:logistic"
        if data.bm_eval_metric is not None:
            params["eval_metric"] = data.bm_eval_metric
    elif data.task == "Learning to rank":
        params["objective"] = "rank:ndcg"
        params["eval_metric"] = data.bm_eval_metric or "ndcg@10"
    else:
        raise ValueError("Unknown task: " + data.task)

    return params


def configure_lightgbm(data, use_gpu):
    params = {
        'task': 'train',
        'boosting_type': 'gbdt',
        'max_depth': _tree_max_depth(data),
        'num_leaves': 2 ** 8,
        'learning_rate': learning_rate, 'min_data_in_leaf': 0,
        'min_sum_hessian_in_leaf': 1, 'lambda_l2': 1, 'min_split_gain': min_split_loss,
        'min_child_weight': min_weight, 'lambda_l1': l1_reg, 'lambda_l2': l2_reg}

    if use_gpu:
        params["device"] = "gpu"

    if data.task == "Regression":
        params["objective"] = "regression"
    elif data.task == "Multiclass classification":
        params["objective"] = "multiclass"
        params["num_class"] = data.num_classes
    elif data.task == "Classification":
        params["objective"] = "binary"
    elif data.task == "Learning to rank":
        params["objective"] = "lambdarank"
        params["metric"] = "ndcg"
    else:
        raise ValueError("Unknown task: " + data.task)

    return params


def configure_catboost(data, use_gpu, args):
    if int(args.n_gpus) == -1:
        dev_arr = "-1"
    else:
        dev_arr = [i for i in range(0, int(args.n_gpus))]

    params = {
        'learning_rate': learning_rate,
        'depth': _tree_max_depth(data),
        'l2_leaf_reg': l2_reg,
        'devices': dev_arr,
    }
    if use_gpu:
        params['task_type'] = 'GPU'
    if data.task == "Multiclass classification":
        params['loss_function'] = 'MultiClass'
        params["classes_count"] = data.num_classes
        params["eval_metric"] = 'MultiClass'
    elif data.task == "Classification" and data.bm_eval_metric == "auc":
        params["eval_metric"] = "AUC"
    return params


def run_xgboost(data, params, args):
    if getattr(data, "qid_train", None) is not None:
        dtrain = xgb.DMatrix(data.X_train, label=data.y_train)
        dtrain.set_group(_groups_from_qid(data.qid_train))
        dval = xgb.DMatrix(data.X_val, label=data.y_val)
        dval.set_group(_groups_from_qid(data.qid_val))
        dtest = xgb.DMatrix(data.X_test, label=data.y_test)
        dtest.set_group(_groups_from_qid(data.qid_test))
    else:
        dtrain = xgb.DMatrix(data.X_train, data.y_train)
        dval = xgb.DMatrix(data.X_val, data.y_val)
        dtest = xgb.DMatrix(data.X_test, data.y_test)
    dev = params.get("device", "cpu")
    print(
        "xgb ({}, {}): training {} rounds, train/val/test rows {:,} / {:,} / {:,}".format(
            dev,
            params.get("tree_method"),
            args.num_rounds,
            data.X_train.shape[0],
            data.X_val.shape[0],
            data.X_test.shape[0],
        ),
        flush=True,
    )
    start = time.time()
    bst = xgb.train(
        params,
        dtrain,
        num_boost_round=args.num_rounds,
        evals=[(dtrain, "train"), (dval, "val")],
    )
    elapsed = time.time() - start
    print(
        "xgb: training done in {:.3f}s; predicting on {:,} test rows (no progress bar)...".format(
            elapsed,
            data.X_test.shape[0],
        ),
        flush=True,
    )
    pred = bst.predict(dtest)
    print("xgb: predict done; computing metric.", flush=True)
    metric = eval(data, pred)
    return elapsed, metric


def _xgboost_tree_method(alg):
    if "-approx" in alg:
        return "approx"
    return "hist"


def train_xgboost(alg, data, df, args):
    if alg not in args.algs:
        return
    if xgb is None:
        print(f"Skipping {alg}: XGBoost not installed")
        return
    use_gpu = True if 'gpu' in alg else False
    params = configure_xgboost(data, use_gpu, args, tree_method=_xgboost_tree_method(alg))
    elapsed, metric = run_xgboost(data, params, args)
    add_data(df, alg, data, elapsed, metric)


def run_lightgbm(data, params, args):
    if getattr(data, "qid_train", None) is not None:
        lgb_train = lgb.Dataset(
            data.X_train,
            data.y_train,
            group=_groups_from_qid(data.qid_train),
        )
        lgb_eval = lgb.Dataset(
            data.X_val,
            data.y_val,
            group=_groups_from_qid(data.qid_val),
            reference=lgb_train,
        )
    else:
        lgb_train = lgb.Dataset(data.X_train, data.y_train)
        lgb_eval = lgb.Dataset(data.X_test, data.y_test, reference=lgb_train)
    start = time.time()
    gbm = lgb.train(params,
                    lgb_train,
                    num_boost_round=args.num_rounds,
                    valid_sets=lgb_eval)
    elapsed = time.time() - start
    pred = gbm.predict(data.X_test)
    metric = eval(data, pred)
    return elapsed, metric


def train_lightgbm(alg, data, df, args):
    if alg not in args.algs:
        return
    if lgb is None:
        print(f"Skipping {alg}: LightGBM not installed")
        return
    use_gpu = True if 'gpu' in alg else False
    params = configure_lightgbm(data, use_gpu)
    elapsed, metric = run_lightgbm(data, params, args)
    add_data(df, alg, data, elapsed, metric)


def run_catboost(data, params, args):
    cat_train = cat.Pool(data.X_train, data.y_train)
    cat_test = cat.Pool(data.X_test, data.y_test)
    cat_val = cat.Pool(data.X_val, data.y_val)

    params['iterations'] = args.num_rounds

    if data.task == "Regression":
        model = cat.CatBoostRegressor(**params)
    else:
        model = cat.CatBoostClassifier(**params)

    start = time.time()
    model.fit(cat_train, use_best_model=False, eval_set=cat_val)
    elapsed = time.time() - start

    if data.task == "Multiclass classification":
        preds = model.predict_proba(cat_test)
    elif data.metric == "AUC":
        preds = model.predict_proba(cat_test)[:, 1]
    else:
        preds = model.predict(cat_test)

    metric = eval(data, preds)
    return elapsed, metric


def train_catboost(alg, data, df, args):
    if alg not in args.algs:
        return
    if cat is None:
        print(f"Skipping {alg}: CatBoost not installed")
        return
    use_gpu = True if 'gpu' in alg else False

    if data.task == "Learning to rank":
        add_data(df, alg, data, float("nan"), float("nan"))
        return

    # catboost GPU does not work with multiclass
    if data.task == "Multiclass classification" and use_gpu:
        add_data(df, alg, data, 'N/A', 'N/A')
        return

    params = configure_catboost(data, use_gpu, args)
    elapsed, metric = run_catboost(data, params, args)
    add_data(df, alg, data, elapsed, metric)


class Experiment:
    def __init__(
        self,
        data_func,
        name,
        task,
        metric,
        bm_max_depth=None,
        bm_eval_metric=None,
    ):
        self.data_func = data_func
        self.name = name
        self.task = task
        self.metric = metric
        self.bm_max_depth = bm_max_depth
        self.bm_eval_metric = bm_eval_metric

    def run(self, df, args):
        if self.name in ("Bosch", "PeerJ Bosch"):
            ku = args.kaggle_username or os.environ.get("KAGGLE_USERNAME")
            kk = args.kaggle_key or os.environ.get("KAGGLE_KEY")
            if ku and kk:
                loaded = self.data_func(
                    num_rows=args.rows, kaggle_username=ku, kaggle_key=kk
                )
            else:
                loaded = self.data_func(num_rows=args.rows)
        else:
            loaded = self.data_func(num_rows=args.rows)

        if self.task == "Learning to rank":
            X, y, qid = loaded
            data = RankingData(
                X,
                y,
                qid,
                self.name,
                self.metric,
                bm_max_depth=self.bm_max_depth,
                bm_eval_metric=self.bm_eval_metric or "ndcg@10",
            )
        else:
            X, y = loaded
            data = Data(
                X,
                y,
                self.name,
                self.task,
                self.metric,
                bm_max_depth=self.bm_max_depth,
                bm_eval_metric=self.bm_eval_metric,
            )
        train_xgboost('xgb-cpu-hist', data, df, args)
        train_xgboost('xgb-gpu-hist', data, df, args)
        train_xgboost('xgb-cpu-approx', data, df, args)
        train_xgboost('xgb-gpu-approx', data, df, args)
        train_lightgbm('lightgbm-cpu', data, df, args)
        train_lightgbm('lightgbm-gpu', data, df, args)
        train_catboost('cat-cpu', data, df, args)
        train_catboost('cat-gpu', data, df, args)


# PeerJ (2017) GPU XGBoost workloads — https://doi.org/10.7717/peerj-cs.127
def build_experiments(datasets_root=None, yltr_train_file=None, bosch_zip=None):
    """
    Wire local Bosch / Yahoo YLTR paths. PeerJ YLTR uses Yahoo data under datasets_root/yltr
    when present (or --yltr_train_file); otherwise falls back to MQ2008 inside the loader.
    """

    def bosch_load(num_rows=None, kaggle_username=None, kaggle_key=None):
        return data_loader.get_bosch(
            num_rows,
            kaggle_username,
            kaggle_key,
            data_root=datasets_root,
            bosch_bundle_path=bosch_zip,
        )

    def yltr_load(num_rows=None):
        return data_loader.get_peerj_yltr_ranking(
            num_rows,
            data_root=datasets_root,
            train_file=yltr_train_file,
        )

    return [
        Experiment(data_loader.get_year, "YearPredictionMSD", "Regression", "RMSE"),
        Experiment(data_loader.get_synthetic_regression, "Synthetic", "Regression", "RMSE"),
        Experiment(data_loader.get_higgs, "Higgs", "Classification", "Accuracy"),
        Experiment(
            data_loader.get_cover_type, "Cover Type", "Multiclass classification", "Accuracy"
        ),
        Experiment(bosch_load, "Bosch", "Classification", "Accuracy"),
        Experiment(data_loader.get_airline, "Airline", "Classification", "Accuracy"),
        Experiment(
            yltr_load,
            "PeerJ YLTR",
            "Learning to rank",
            "NDCG@10",
            bm_max_depth=6,
            bm_eval_metric="ndcg@10",
        ),
        Experiment(
            data_loader.get_higgs,
            "PeerJ Higgs",
            "Classification",
            "AUC",
            bm_max_depth=12,
            bm_eval_metric="auc",
        ),
        Experiment(
            bosch_load,
            "PeerJ Bosch",
            "Classification",
            "AUC",
            bm_max_depth=6,
            bm_eval_metric="auc",
        ),
    ]


_DATASET_NAME_ALIASES = {
    "PeerJ YLTR (MQ2008)": "PeerJ YLTR",
}


def write_results(df, filename, format):
    if format == "latex":
        tmp_df = df.copy()
        if not isinstance(tmp_df.columns, pd.MultiIndex):
            tuple_cols = [c for c in tmp_df.columns if isinstance(c, tuple)]
            if len(tuple_cols) != len(tmp_df.columns):
                tmp_df = tmp_df[tuple_cols]
            tmp_df.columns = pd.MultiIndex.from_tuples(list(tmp_df.columns))
        with open(filename, "w") as file:
            file.write(tmp_df.to_latex())
    elif format == "csv":
        with open(filename, "w") as file:
            file.write(df.to_csv())
    else:
        raise ValueError("Unknown format: " + format)

    print(format + " results written to: " + filename)


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--rows',
        type=int,
        default=None,
        help=(
            'Max rows per dataset loader. If omitted, each dataset uses its full default '
            '(Synthetic uses 10,000,000 rows and will be very slow). Example: --rows 100000'
        ),
    )
    parser.add_argument('--num_rounds', type=int, default=500, help='Boosting rounds.')
    parser.add_argument(
        '--datasets_root',
        default=os.environ.get("GBM_DATASETS_ROOT"),
        help=(
            'Local datasets directory (e.g. /path/to/xgboost_stuff/datasets). '
            'Expects Bosch zip or train_numeric.csv.zip in this folder, and yltr/ for Yahoo LTR. '
            'Override with GBM_DATASETS_ROOT.'
        ),
    )
    parser.add_argument(
        '--yltr_train_file',
        default=None,
        help=(
            'Explicit path to Yahoo LTR training file (svmlight + qid). '
            'If unset, looks under DATASETS_ROOT/yltr for set1.train.txt or extracts yltr/*.tgz.'
        ),
    )
    parser.add_argument(
        '--bosch_zip',
        default=None,
        help=(
            'Explicit path to train_numeric.csv.zip or full bosch-production-line-performance.zip.'
        ),
    )
    parser.add_argument(
        '--datasets',
        default=None,
        help=(
            'Comma-separated exact dataset names (no substring matching). '
            'Default: all experiments. Alias: PeerJ YLTR (MQ2008) -> PeerJ YLTR.'
        ),
    )
    parser.add_argument('--debug_verbose', type=int, default=1)
    parser.add_argument('--n_gpus', type=int, default=-1)
    parser.add_argument(
        '--algs',
        default=(
            'xgb-cpu-hist,xgb-gpu-hist,xgb-cpu-approx,xgb-gpu-approx,'
            'lightgbm-cpu,lightgbm-gpu,cat-cpu,cat-gpu'
        ),
        help='Boosting algorithms to run (xgb: *-hist or *-approx).',
    )
    parser.add_argument(
        '--kaggle_username',
        default=None,
        help='Kaggle API username for Bosch download (optional; else KAGGLE_USERNAME or ~/.kaggle/kaggle.json).',
    )
    parser.add_argument(
        '--kaggle_key',
        default=None,
        help='Kaggle API key (optional; else KAGGLE_KEY or ~/.kaggle/kaggle.json). Prefer env over CLI.',
    )
    args = parser.parse_args()
    experiments = build_experiments(
        datasets_root=args.datasets_root,
        yltr_train_file=args.yltr_train_file,
        bosch_zip=args.bosch_zip,
    )
    if args.datasets is None:
        args.datasets = ",".join(exp.name for exp in experiments) + ","
    df = pd.DataFrame()
    raw_pick = {p.strip() for p in args.datasets.split(",") if p.strip()}
    dataset_pick = set(raw_pick)
    for old, new in _DATASET_NAME_ALIASES.items():
        if old in dataset_pick:
            dataset_pick.add(new)
    for exp in experiments:
        if exp.name in dataset_pick:
            exp.run(df, args)
            # Write partial results at each iteration in case of failure
            print(df.to_string())
            write_results(df, "results.latex", "latex")
            write_results(df, "results.csv", "csv")


if __name__ == "__main__":
    main()
