"""Module for loading preprocessed datasets for machine learning problems"""
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import zipfile
from contextlib import contextmanager
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn import datasets
from joblib import Memory

if sys.version_info[0] >= 3:
    from urllib.request import urlretrieve  # pylint: disable=import-error,no-name-in-module
else:
    from urllib import urlretrieve  # pylint: disable=import-error,no-name-in-module

mem = Memory("./mycache")

get_airline_url = 'http://kt.ijs.si/elena_ikonomovska/datasets/airline/airline_14col.data.bz2'

_TRAIN_NUMERIC_ZIP = "train_numeric.csv.zip"
_BOSCH_COMPETITION_ZIP_NAME = "bosch-production-line-performance.zip"


def _read_bosch_numeric_zip(path, num_rows=None):
    """Load X, y from a train_numeric.csv.zip on disk."""
    X = pd.read_csv(
        path, index_col=0, compression="zip", dtype=np.float32, nrows=num_rows
    )
    y = X.iloc[:, -1].values
    X.drop(X.columns[-1], axis=1, inplace=True)
    return X, y


def _resolve_bosch_numeric_zip_path(data_root=None, bosch_bundle_path=None):
    """
    Return path to train_numeric.csv.zip, or None.

    Resolution: explicit bosch_bundle_path, env BOSCH_TRAIN_NUMERIC_ZIP,
    data_root/train_numeric.csv.zip, data_root/bosch zip (extract inner to temp),
    then standard _find_train_numeric_zip().
    """
    if bosch_bundle_path:
        p = Path(bosch_bundle_path).expanduser().resolve()
        if not p.is_file():
            raise FileNotFoundError("bosch_bundle_path not found: {}".format(p))
        if p.name == _TRAIN_NUMERIC_ZIP or p.suffixes == [".csv", ".zip"]:
            return str(p)
        if p.suffix.lower() == ".zip" and "bosch" in p.name.lower():
            tdir = tempfile.mkdtemp(prefix="bosch_inner_")
            inner = _TRAIN_NUMERIC_ZIP
            with zipfile.ZipFile(p, "r") as outer:
                if inner not in outer.namelist():
                    raise FileNotFoundError(
                        "{} missing {} member".format(p, inner)
                    )
                dest = Path(tdir) / inner
                dest.write_bytes(outer.read(inner))
            return str(dest)
        return str(p)

    env = os.environ.get("BOSCH_TRAIN_NUMERIC_ZIP")
    if env:
        ep = Path(env).expanduser()
        if ep.is_file():
            return str(ep)

    if data_root:
        root = Path(data_root).expanduser().resolve()
        direct = root / _TRAIN_NUMERIC_ZIP
        if direct.is_file():
            return str(direct)
        bundle = root / _BOSCH_COMPETITION_ZIP_NAME
        if bundle.is_file():
            tdir = tempfile.mkdtemp(prefix="bosch_bundle_")
            inner = _TRAIN_NUMERIC_ZIP
            with zipfile.ZipFile(bundle, "r") as outer:
                if inner not in outer.namelist():
                    raise FileNotFoundError(
                        "{} missing {} (got: {})".format(
                            bundle, inner, outer.namelist()[:10]
                        )
                    )
                dest = Path(tdir) / inner
                dest.write_bytes(outer.read(inner))
            return str(dest)

    found = _find_train_numeric_zip()
    return found


def _find_train_numeric_zip():
    """Resolve Bosch Kaggle file without requiring CWD."""
    candidates = []
    env = os.environ.get("BOSCH_TRAIN_NUMERIC_ZIP")
    if env:
        candidates.append(Path(env).expanduser())
    candidates.append(Path.cwd() / _TRAIN_NUMERIC_ZIP)
    _here = Path(__file__).resolve().parent
    candidates.append(_here / _TRAIN_NUMERIC_ZIP)
    candidates.append(_here.parent / _TRAIN_NUMERIC_ZIP)
    for p in candidates:
        if p.is_file():
            return str(p)
    return None


@contextmanager
def _kaggle_creds_context(kaggle_username=None, kaggle_key=None):
    """Temporarily set KAGGLE_USERNAME / KAGGLE_KEY for downloads (optional)."""
    if kaggle_username is None and kaggle_key is None:
        yield
        return
    if kaggle_username is None or kaggle_key is None:
        raise ValueError("kaggle_username and kaggle_key must both be set or both omitted.")
    saved = {}
    try:
        for key, val in (
            ("KAGGLE_USERNAME", kaggle_username),
            ("KAGGLE_KEY", kaggle_key),
        ):
            saved[key] = os.environ.get(key)
            os.environ[key] = val
        yield
    finally:
        for key, old in saved.items():
            if old is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = old


def _download_bosch_train_numeric():
    """
    Fetch train_numeric.csv.zip using the Kaggle CLI if present, else the Kaggle Python API
    (same credentials as ~/.kaggle/kaggle.json or env vars).
    """
    download_dir = Path.cwd()
    if shutil.which("kaggle"):
        subprocess.run(
            [
                "kaggle",
                "competitions",
                "download",
                "-c",
                "bosch-production-line-performance",
                "-f",
                _TRAIN_NUMERIC_ZIP,
                "-p",
                ".",
            ],
            cwd=str(download_dir),
            check=False,
        )
        if _find_train_numeric_zip():
            return True
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
    except ImportError:
        return False
    api = KaggleApi()
    api.authenticate()
    try:
        api.competition_download_file(
            "bosch-production-line-performance",
            _TRAIN_NUMERIC_ZIP,
            path=str(download_dir),
            quiet=False,
        )
    except Exception as exc:
        from requests.exceptions import HTTPError

        code = getattr(getattr(exc, "response", None), "status_code", None)
        if isinstance(exc, HTTPError) and code in (401, 403):
            raise RuntimeError(
                "Kaggle API refused the Bosch download (HTTP {}). "
                "Fix: (1) Regenerate API token on Kaggle (Account -> API -> Create New Token) "
                "and update ~/.kaggle/kaggle.json or KAGGLE_USERNAME/KAGGLE_KEY; "
                "(2) Open the competition page and accept the rules: "
                "https://www.kaggle.com/c/bosch-production-line-performance ; "
                "(3) Ensure username matches your Kaggle profile exactly.".format(code)
            ) from exc
        raise
    return _find_train_numeric_zip() is not None


@mem.cache
def get_airline(num_rows=None):
    """
    Airline dataset (http://kt.ijs.si/elena_ikonomovska/data.html)

    Has categorical columns converted to ordinal and target variable "Arrival Delay" converted
    to binary target.

    - Dimensions: 115M rows, 13 columns.
    - Task: Binary classification

    :param num_rows:
    :return: X, y
    """
    filename = 'airline_14col.data.bz2'
    if not os.path.isfile(filename):
        urlretrieve(get_airline_url, filename)

    cols = [
        "Year", "Month", "DayofMonth", "DayofWeek", "CRSDepTime",
        "CRSArrTime", "UniqueCarrier", "FlightNum", "ActualElapsedTime",
        "Origin", "Dest", "Distance", "Diverted", "ArrDelay"
    ]

    # load the data as int16
    dtype = np.int16

    dtype_columns = {
        "Year": dtype, "Month": dtype, "DayofMonth": dtype, "DayofWeek": dtype,
        "CRSDepTime": dtype, "CRSArrTime": dtype, "FlightNum": dtype,
        "ActualElapsedTime": dtype, "Distance":
            dtype,
        "Diverted": dtype, "ArrDelay": dtype,
    }

    df = pd.read_csv(filename,
                     names=cols, dtype=dtype_columns, nrows=num_rows)

    # Encode categoricals as numeric
    for col in df.select_dtypes(['object']).columns:
        df[col] = df[col].astype("category").cat.codes

    # Turn into binary classification problem
    df["ArrDelayBinary"] = 1 * (df["ArrDelay"] > 0)

    X = df[df.columns.difference(["ArrDelay", "ArrDelayBinary"])]
    y = df["ArrDelayBinary"]

    del df
    return X, y


get_higgs_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00280/HIGGS.csv.gz'  # pylint: disable=line-too-long


@mem.cache
def get_higgs(num_rows=None):
    """
    Higgs dataset from UCI machine learning repository (
    https://archive.ics.uci.edu/ml/datasets/HIGGS).

    - Dimensions: 11M rows, 28 columns.
    - Task: Binary classification

    :param num_rows:
    :return: X, y
    """
    filename = 'HIGGS.csv.gz'
    if not os.path.isfile(filename):
        urlretrieve(get_higgs_url, filename)
    higgs = pd.read_csv(filename, nrows=num_rows)
    X = higgs.iloc[:, 1:].values
    y = higgs.iloc[:, 0].values

    return X, y


MQ2008_URL = "https://s3-us-west-2.amazonaws.com/xgboost-examples/MQ2008.zip"


@mem.cache
def get_mq2008_ranking(num_rows=None):
    """
    MS LETOR MQ2008 Fold1 train (public). PeerJ (2017) used Yahoo LTR (YLTR) with
    rank:ndcg / ndcg@10; this is a standard public learning-to-rank substitute.

    Returns (X, y, qid) with rows sorted by qid. Truncates to num_rows on a query boundary.
    """
    from sklearn.datasets import load_svmlight_file

    dpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "peerj_ltr_data")
    os.makedirs(dpath, exist_ok=True)
    zpath = os.path.join(dpath, "MQ2008.zip")
    if not os.path.isfile(zpath):
        print("Downloading MQ2008.zip for PeerJ-style LTR workload...", flush=True)
        urlretrieve(MQ2008_URL, zpath)
    with zipfile.ZipFile(zpath, "r") as zf:
        zf.extractall(dpath)
    train_path = os.path.join(dpath, "MQ2008", "Fold1", "train.txt")
    X, y, qid = load_svmlight_file(train_path, query_id=True, dtype=np.float32)
    X = X.toarray()
    y = y.astype(np.float32)
    qid = qid.astype(np.int64)
    order = np.argsort(qid, kind="mergesort")
    X, y, qid = X[order], y[order], qid[order]
    if num_rows is not None and num_rows < X.shape[0]:
        end = num_rows
        while end < X.shape[0] and qid[end] == qid[end - 1]:
            end += 1
        X, y, qid = X[:end], y[:end], qid[:end]
    return X, y, qid


@mem.cache
def get_cover_type(num_rows=None):
    """
    Cover type dataset from UCI machine learning repository (
    https://archive.ics.uci.edu/ml/datasets/covertype).

    y contains 7 unique class labels from 1 to 7 inclusive.

    - Dimensions: 581012 rows, 54 columns.
    - Task: Multiclass classification

    :param num_rows:
    :return: X, y
    """
    data = datasets.fetch_covtype()
    X = data.data
    y = data.target
    if num_rows is not None:
        X = X[0:num_rows]
        y = y[0:num_rows]

    return X, y


@mem.cache
def get_synthetic_regression(num_rows=None):
    """
    Synthetic regression generator from sklearn (
    http://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_regression.html).

    - Dimensions: 10000000 rows, 100 columns.
    - Task: Regression

    :param num_rows:
    :return: X, y
    """
    if num_rows is None:
        num_rows = 10000000
    print(
        "get_synthetic_regression: generating {:,} samples (100 features); "
        "omit with --rows N for a smaller, faster run.".format(num_rows),
        flush=True,
    )
    return datasets.make_regression(n_samples=num_rows, bias=100, noise=1.0, random_state=0)


get_year_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00203/YearPredictionMSD.txt.zip'  # pylint: disable=line-too-long


@mem.cache
def get_year(num_rows=None):
    """
    YearPredictionMSD dataset from UCI repository (
    https://archive.ics.uci.edu/ml/datasets/yearpredictionmsd)

    - Dimensions: 515345 rows, 90 columns.
    - Task: Regression

    :param num_rows:
    :return: X,y
    """
    filename = 'YearPredictionMSD.txt.zip'
    if not os.path.isfile(filename):
        urlretrieve(get_year_url, filename)

    year = pd.read_csv(filename, header=None, nrows=num_rows)
    X = year.iloc[:, 1:].values
    y = year.iloc[:, 0].values
    return X, y


get_url_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/url/url_svmlight.tar.gz'  # pylint: disable=line-too-long


@mem.cache
def get_url(num_rows=None):
    """
    URL reputation dataset from UCI repository (
    https://archive.ics.uci.edu/ml/datasets/URL+Reputation)

    Extremely sparse classification dataset. X is returned as a scipy sparse matrix.

    - Dimensions: 2396130 rows, 3231961 columns.
    - Task: Classification

    :param num_rows:
    :return: X,y
    """
    from scipy.sparse import vstack
    filename = 'url_svmlight.tar.gz'
    if not os.path.isfile(filename):
        urlretrieve(get_url_url, filename)
        tar = tarfile.open(filename, "r:gz")
        tar.extractall()
        tar.close()

    num_files = 120
    files = ['url_svmlight/Day{}.svm'.format(day) for day in range(num_files)]
    data = datasets.load_svmlight_files(files)
    X = vstack(data[::2])
    y = np.concatenate(data[1::2])

    y[y < 0.0] = 0.0

    if num_rows is not None:
        X = X[0:num_rows]
        y = y[0:num_rows]

    return X, y


@mem.cache
def _load_bosch_from_zip(num_rows=None):
    """Load Bosch frame from disk; cached on ``num_rows`` only (no credentials)."""
    path = _find_train_numeric_zip()
    if path is None:
        raise RuntimeError("internal: Bosch zip missing after download")
    return _read_bosch_numeric_zip(path, num_rows)


def get_bosch(
    num_rows=None,
    kaggle_username=None,
    kaggle_key=None,
    data_root=None,
    bosch_bundle_path=None,
):
    """
    Bosch Production Line Performance data set (
    https://www.kaggle.com/c/bosch-production-line-performance)

    Data file: ``train_numeric.csv.zip`` (Kaggle competition file). Resolution order:
    ``bosch_bundle_path`` (train zip or full competition zip),
    ``$BOSCH_TRAIN_NUMERIC_ZIP``,
    ``data_root/train_numeric.csv.zip`` or ``data_root/bosch-production-line-performance.zip``,
    then current working directory / package dirs. If still missing, Kaggle download.

    :param data_root: Optional base directory (e.g. local datasets folder).
    :param bosch_bundle_path: Optional explicit path to ``train_numeric.csv.zip`` or
        ``bosch-production-line-performance.zip``.
    :return: X,y
    """
    path = _resolve_bosch_numeric_zip_path(
        data_root=data_root, bosch_bundle_path=bosch_bundle_path
    )
    if path is None:
        with _kaggle_creds_context(kaggle_username, kaggle_key):
            _download_bosch_train_numeric()
        path = _resolve_bosch_numeric_zip_path(
            data_root=data_root, bosch_bundle_path=bosch_bundle_path
        )
    if path is None:
        raise FileNotFoundError(
            "Bosch dataset: {} not found after Kaggle download attempts. "
            "Place train_numeric.csv.zip or {} under --datasets_root, set "
            "BOSCH_TRAIN_NUMERIC_ZIP, or use --bosch_zip. Or use --datasets without Bosch.".format(
                _TRAIN_NUMERIC_ZIP, _BOSCH_COMPETITION_ZIP_NAME
            )
        )
    return _read_bosch_numeric_zip(path, num_rows)


def _find_yahoo_yltr_train_file(data_root):
    """Return path to pre-extracted Yahoo LTR train svmlight file, or None."""
    yltr = Path(data_root).expanduser().resolve() / "yltr"
    if not yltr.is_dir():
        return None
    preferred = [
        yltr / "set1.train.txt",
        yltr / "set2.train.txt",
        yltr / "Yahoo-Learning-to-Rank-Challenge" / "set1.train.txt",
        yltr / "Yahoo-Learning-to-Rank-Challenge" / "set2.train.txt",
    ]
    for p in preferred:
        if p.is_file():
            return p
    for name in ("set1.train.txt", "set2.train.txt"):
        hits = [p for p in yltr.rglob(name) if p.is_file() and ".git" not in p.parts]
        if hits:
            return hits[0]
    hits = [
        p
        for p in yltr.rglob("*.txt")
        if p.is_file()
        and ".git" not in p.parts
        and "train" in p.name.lower()
        and p.stat().st_size > 500_000
    ]
    return hits[0] if hits else None


def _ensure_yahoo_tgz_extracted(data_root, cache_dir):
    """
    If ``yltr`` contains a ``*.tgz`` bundle (Yahoo Learning-to-Rank Challenge layout),
    extract nested archives into cache_dir and return path to a train svmlight file.
    """
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    marker = cache_dir / ".yahoo_full_extract_ok"
    yltr = Path(data_root).expanduser().resolve() / "yltr"
    if not yltr.is_dir():
        return None
    outer = None
    for p in sorted(yltr.rglob("*.tgz")):
        if ".git" in p.parts:
            continue
        outer = p
        break
    if outer is None:
        return None
    stage = cache_dir / "yahoo_stage"
    unpack = cache_dir / "yahoo_ltr_unpacked"
    if not marker.is_file():
        if stage.exists():
            shutil.rmtree(stage, ignore_errors=True)
        if unpack.exists():
            shutil.rmtree(unpack, ignore_errors=True)
        stage.mkdir(parents=True)
        with tarfile.open(outer, "r:*") as tf:
            tf.extractall(stage)
        inner = next(stage.rglob("ltrc_yahoo.tar.bz2"), None)
        if inner is None:
            return None
        unpack.mkdir(parents=True)
        with tarfile.open(inner, "r:bz2") as tf:
            tf.extractall(unpack)
        marker.write_text(str(outer), encoding="utf-8")
    for name in ("set1.train.txt", "set2.train.txt"):
        hits = list(unpack.rglob(name))
        if hits:
            return hits[0]
    hits = [
        p
        for p in unpack.rglob("*.txt")
        if p.is_file()
        and "train" in p.name.lower()
        and p.stat().st_size > 500_000
    ]
    return hits[0] if hits else None


@mem.cache
def get_peerj_yltr_ranking(num_rows=None, data_root=None, train_file=None):
    """
    Yahoo Learning-to-Rank (PeerJ YLTR workload): load local svmlight + qid.

    Resolution: ``train_file`` if set; else ``data_root/yltr/**`` pre-extracted
    ``set1.train.txt`` / ``set2.train.txt``; else extract ``yltr/**/*.tgz`` into package
    cache (nested ``ltrc_yahoo.tar.bz2``); else fall back to :func:`get_mq2008_ranking`.

    Returns (X, y, qid) dense float X, sorted by qid.
    """
    from sklearn.datasets import load_svmlight_file

    train_path = None
    if train_file:
        train_path = Path(train_file).expanduser().resolve()
        if not train_path.is_file():
            raise FileNotFoundError("yltr train_file not found: {}".format(train_path))
    elif data_root:
        root = Path(data_root).expanduser().resolve()
        train_path = _find_yahoo_yltr_train_file(root)
        if train_path is None:
            cache_dir = Path(__file__).resolve().parent / "yahoo_ltr_cache"
            train_path = _ensure_yahoo_tgz_extracted(root, cache_dir)
    if train_path is None or not train_path.is_file():
        print(
            "Yahoo YLTR train file not found under data_root; using MQ2008 substitute.",
            flush=True,
        )
        return get_mq2008_ranking(num_rows)
    print("Loading PeerJ YLTR from {}".format(train_path), flush=True)
    X, y, qid = load_svmlight_file(str(train_path), query_id=True, dtype=np.float32)
    if hasattr(X, "toarray"):
        X = X.toarray()
    y = y.astype(np.float32)
    qid = qid.astype(np.int64)
    order = np.argsort(qid, kind="mergesort")
    X, y, qid = X[order], y[order], qid[order]
    if num_rows is not None and num_rows < X.shape[0]:
        end = num_rows
        while end < X.shape[0] and qid[end] == qid[end - 1]:
            end += 1
        X, y, qid = X[:end], y[:end], qid[:end]
    return X, y, qid
