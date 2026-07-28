# GBM-Benchmarks

Multi-algorithm Gradient Boosting Machine (GBM) benchmark suite, used to evaluate **XGBoost on AMD Instinct™ GPUs with the ROCm HIP build** alongside CPU baselines (and optional LightGBM / CatBoost cross-library context).

The entry point `benchmark.py` loads each dataset via `ml_dataset_loader`, splits train/validation/test, configures the right XGBoost objective for the task, runs `xgboost.train` for each requested algorithm flag, and writes per-dataset wall-clock and metric results to `results.csv` / `results.latex`.

> **Provenance.** The benchmark scripts in this directory (`benchmark.py`, `install_gbm.sh`, `ml_dataset_loader/`) are **modified versions of the upstream suite at [RAMitchell/GBM-Benchmarks](https://github.com/RAMitchell/GBM-Benchmarks)**. The ROCm port adds XGBoost 3.x compatibility (`device=` / `tree_method=hist|approx`), the `approx` flags on CPU and GPU, the PeerJ-style ranking / AUC experiments, learning-to-rank group handling, label encoding for stable multi-class GPU runs, local-path support for Bosch and Yahoo LTR data, and AMD Instinct-aware defaults.

## Requirements

- **AMD Instinct GPU** (CDNA 3 / MI300-series recommended) and a working **ROCm 7.0** stack (`rocm-smi`, `amdgpu` driver, `HIP_VISIBLE_DEVICES`).
- **XGBoost 3.2.0 ROCm HIP build** importable as `import xgboost`.
- **Python 3** with `numpy`, `pandas`, `scikit-learn`.
- *Optional*: `lightgbm`, `catboost` (only needed if you pass `lightgbm-*` / `cat-*` to `--algs`).
- *Optional*: [Kaggle CLI](https://github.com/Kaggle/kaggle-api) credentials for the `Bosch` / `PeerJ Bosch` experiments (or a pre-downloaded zip via `--bosch_zip`).

## Usage

```sh
python3 benchmark.py [-h] [--rows ROWS] [--num_rounds NUM_ROUNDS]
                     [--datasets_root DATASETS_ROOT]
                     [--yltr_train_file YLTR_TRAIN_FILE]
                     [--bosch_zip BOSCH_ZIP]
                     [--datasets DATASETS] [--algs ALGS]
                     [--debug_verbose DEBUG_VERBOSE] [--n_gpus N_GPUS]
                     [--kaggle_username KAGGLE_USERNAME]
                     [--kaggle_key KAGGLE_KEY]
```

| Flag | Default | Notes |
| :--- | :------ | :---- |
| `--rows` | `None` (full) | Cap rows per dataset. Useful for smoke tests. `Synthetic` defaults to 10 M rows when uncapped. |
| `--num_rounds` | `500` | Boosting rounds passed to `xgboost.train`. |
| `--datasets_root` | `$GBM_DATASETS_ROOT` | Local datasets directory (Bosch zip, `yltr/` subfolder, etc.). |
| `--yltr_train_file` | `None` | Explicit path to a Yahoo LTR svmlight + qid file. |
| `--bosch_zip` | `None` | Explicit path to `train_numeric.csv.zip` or the full Bosch zip. |
| `--datasets` | all 9 | Comma-separated **exact** experiment names (see [Experiments](#experiments)). |
| `--algs` | all 8 | `xgb-cpu-hist,xgb-gpu-hist,xgb-cpu-approx,xgb-gpu-approx,lightgbm-cpu,lightgbm-gpu,cat-cpu,cat-gpu`. |
| `--n_gpus` | `-1` | CatBoost device list selector (`-1` = all visible GPUs). |
| `--debug_verbose` | `1` | XGBoost `verbosity`. |
| `--kaggle_username` / `--kaggle_key` | — | Bosch download credentials. Env vars `KAGGLE_USERNAME` / `KAGGLE_KEY` are preferred. |

Hyperparameters shared across all XGBoost runs (set at the top of `benchmark.py`): `random_seed=0`, `max_depth=6` (12 for `PeerJ Higgs`), `learning_rate=0.1`, `gamma=0`, `min_child_weight=1`, `alpha=0`, `lambda=1`. ROCm GPU paths use `device="cuda"` — the ROCm HIP build maps that to HIP transparently. Pin a specific Instinct GPU with `HIP_VISIBLE_DEVICES`.

## Algorithms

| `--algs` flag | XGBoost params it sets | Notes |
| :------------ | :--------------------- | :---- |
| `xgb-cpu-hist` | `tree_method=hist`, `device=cpu` | CPU baseline; same algorithm as GPU hist. |
| `xgb-gpu-hist` | `tree_method=hist`, `device=cuda` | **Primary ROCm GPU path** on Instinct. |
| `xgb-cpu-approx` | `tree_method=approx`, `device=cpu` | CPU sketching reference. |
| `xgb-gpu-approx` | `tree_method=approx`, `device=cuda` | GPU sketching reference. |
| `lightgbm-cpu` / `lightgbm-gpu` | LightGBM `gbdt` | Cross-library context. |
| `cat-cpu` / `cat-gpu` | CatBoost `Regressor` / `Classifier` | Cross-library context. CatBoost GPU does not support multiclass and is skipped on `Cover Type`; CatBoost is also skipped for ranking. |

`xgboost::tree::exact` is **CPU-only** in modern XGBoost and is intentionally not exposed as a flag.

## Experiments

`build_experiments()` defines nine experiments mapped one-to-one onto `--datasets` values:

| `--datasets` value | Task | XGBoost objective | Metric | Notes |
| :----------------- | :--- | :---------------- | :----- | :---- |
| `YearPredictionMSD` | Regression | `reg:squarederror` | RMSE | UCI Million Song. |
| `Synthetic` | Regression | `reg:squarederror` | RMSE | 10 M rows by default (use `--rows` to shrink). |
| `Higgs` | Binary classification | `binary:logistic` | Accuracy | UCI HIGGS, ~11 M × 28. |
| `Cover Type` | Multiclass | `multi:softmax` | Accuracy | 7 classes, label-encoded for stable splits. |
| `Bosch` | Binary classification | `binary:logistic` | Accuracy | Kaggle; needs API token or `--bosch_zip`. |
| `Airline` | Binary classification | `binary:logistic` | Accuracy | US airline on-time. |
| `PeerJ YLTR` (alias `PeerJ YLTR (MQ2008)`) | Learning to rank | `rank:ndcg` | NDCG@10 | Yahoo LTR if available under `<datasets_root>/yltr/`, else MQ2008. |
| `PeerJ Higgs` | Binary classification | `binary:logistic` | AUC | `max_depth=12`, AUC eval. |
| `PeerJ Bosch` | Binary classification | `binary:logistic` | AUC | Bosch with AUC eval (needs Kaggle creds / zip). |

Datasets are downloaded on first run and cached under `mycache/`. Allow time on the first invocation.

## Common runs

Three canonical invocation patterns. Replace `<DATASETS_ROOT>` with the absolute path to your local datasets directory (the same value can also be set via the `GBM_DATASETS_ROOT` environment variable to drop the flag entirely).

**1. Full XGBoost-only sweep on ROCm — all rows, 500 rounds default, all 9 datasets**

```sh
python3 benchmark.py \
  --algs "xgb-cpu-approx,xgb-gpu-approx,xgb-gpu-hist,xgb-cpu-hist" \
  --datasets_root <DATASETS_ROOT>
```

**2. Smoke test — small rows / few rounds, explicit dataset list**

```sh
python3 benchmark.py \
  --rows 100 --num_rounds 10 \
  --algs "xgb-cpu-approx,xgb-gpu-approx,xgb-gpu-hist,xgb-cpu-hist" \
  --datasets_root <DATASETS_ROOT> \
  --datasets "PeerJ YLTR (MQ2008),PeerJ Higgs,YearPredictionMSD,Synthetic,Higgs,Cover Type,Airline,Bosch,PeerJ Bosch,PeerJ YLTR"
```

**3. No-API-token subset** — same smoke test but skipping `Bosch` / `PeerJ Bosch` (which require Kaggle credentials). All other datasets download automatically.

```sh
python3 benchmark.py \
  --rows 100 --num_rounds 10 \
  --algs "xgb-cpu-approx,xgb-gpu-approx,xgb-gpu-hist,xgb-cpu-hist" \
  --datasets "PeerJ YLTR (MQ2008),PeerJ Higgs,YearPredictionMSD,Synthetic,Higgs,Cover Type,Airline"
```

## ROCm tips

- **Pin a single Instinct GPU** for an apples-to-apples GPU run: `HIP_VISIBLE_DEVICES=0 python3 benchmark.py …`. (Multi-GPU XGBoost training is not wired into `benchmark.py`; the legacy `--n_gpus` flag is consumed by CatBoost only.)
- **Profile a single algorithm** with rocprofiler v3:
  ```sh
  rocprofv3 --pmc-kernel-top -- \
      python3 benchmark.py --algs xgb-gpu-hist --datasets Higgs \
                           --rows 1000000 --num_rounds 50
  ```
  Then inspect `pmc_kernel_top.csv`, `pmc_perf.csv`, `roofline.csv` next to the run.
- **Iterate fast** by combining `--rows`, `--num_rounds`, and `--datasets` (e.g. `--datasets Higgs --rows 100000 --num_rounds 50`) before scaling out to the full sweep.
- **Bosch shortcuts:** `--bosch_zip <path-to-train_numeric.csv.zip>` skips the Kaggle API entirely if you already have the archive.
- **`PeerJ YLTR` vs `PeerJ YLTR (MQ2008)`** — the suite treats them as aliases (`_DATASET_NAME_ALIASES`); if no Yahoo LTR data is found under `<datasets_root>/yltr/`, the loader falls back to MQ2008 and the metric column reports NDCG@10 over MQ2008 query groups.

## Reference results on AMD Instinct

End-to-end `xgboost.train` wall-clock (in seconds) on a single GCD, ROCm HIP build of XGBoost 3.2.0, default suite hyperparameters (`num_rounds=500`, `max_depth=6` — except `PeerJ Higgs` which uses `max_depth=12`). Update the `[TBD]` cells as new measurements land.

| Experiment | MI300X `xgb-gpu-hist` (s) | MI300X `xgb-gpu-approx` (s) | MI355 `xgb-gpu-hist` (s) | MI355 `xgb-gpu-approx` (s) |
| :--------- | ------------------------: | --------------------------: | -----------------------: | -------------------------: |
| `YearPredictionMSD` | **1.66** | **3.52** | **1.55** | **9.18** |
| `Synthetic` | **7.01** | **8.63** | **6.12** | **14.48** |
| `Higgs` | **3.83** | **92.83** | **3.22** | **56.51** |
| `Cover Type` | **6.41** | **73.24** | **5.50** | **99.04** |
| `Bosch` | **19.83** | **79.51** | **21.89** | **68.51** |
| `Airline` | **18.33** | **484.43** | **13.56** | **229.28** |
| `PeerJ YLTR` | **3.46** | **98.64** | **3.36** | **59.91** |
| `PeerJ Higgs` | **22.16** | **107.37** | **22.20** | **82.86** |
| `PeerJ Bosch` | **20.23** | **78.96** | **22.30** | **68.87** |

When recording new results, also note ROCm version, XGBoost wheel commit, GPU revision, driver / BIOS, whether the run uses one GCD or the full package, and the `--rows` / `--num_rounds` configuration used.

## Outputs

After each experiment finishes, `benchmark.py` writes (and overwrites) two files in the current working directory:

- `results.csv` — pandas dataframe in CSV form, columns are `(dataset, "Time(s)")` and `(dataset, metric)` for every algorithm/dataset pair seen so far.
- `results.latex` — same dataframe rendered as a LaTeX `tabular`.

Partial results are flushed after **every** experiment, so a long sweep that fails midway still leaves usable timings on disk.
