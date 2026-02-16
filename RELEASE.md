---
myst:
  html_meta:
    "description lang=en": "ROCm-Finance Release Notes"
    "keywords": "amd, rocm, gpu, finance, financial, sdk, gbm, credit, risk, forecast, simulation, trade, stock, optimize, portfolio, time, model"
---

# AMD ROCm Finance 26.02 release notes

We are excited to announce the addition of the CatBoost library to the AMD ROCm™ Finance Toolkit.

```{note}
Catboost is still in early access and should not be used for production workloads.
```

## Release highlights

CatBoost is a high-performance, open-source gradient boosting library that excels in handling categorical
features and delivering robust, accurate models. This integration brings the power of CatBoost to the ROCm
ecosystem, enabling accelerated performance on AMD GPUs for a variety of financial applications.

Key features of this integration include:

* CatBoost is a high-performance machine learning library specifically engineered to handle tabular data with a focus on "plug-and-play" simplicity and superior accuracy. 
* As a member of the gradient boosting family, it distinguishes itself by natively processing categorical variables—like city names or user IDs—without requiring manual preprocessing, while its unique symmetric tree structure ensures exceptionally fast prediction speeds and reduced overfitting. 
* In the finance sector, this makes it a powerhouse for workloads such as fraud detection, credit scoring, and algorithmic trading; it thrives on the messy, high-cardinality categorical data typical of transaction logs and banking records, providing robust and reliable results even when hyperparameter tuning is kept to a minimum.


````{list-table}
:header-rows: 1

* - Library
  - Current Upstream Version
  - Primary Finance Use‑Cases

* - Catboost
  - 1.2.8
  - Credit scoring, fraud detection, customer segmentation, time-series forecasting

* - XGBoost
  - 3.1.1
  - Prediction and feature parallelization, loan default scoring

* - LightGBM
  - 4.6.0.99
  - Portfolio optimization, time‑series forecasting, market‑microstructure analysis

* - ThunderGBM
  - 0.3.16
  - High‑frequency trading, large‑scale scenario simulations
````

## Supported platforms

To learn about hardware and software environment requirements, see the
{doc}`/about/compatibility-matrix` and the {doc}`/install/prerequisites`.

```{note}
LightGBM and ThunderGBM, are currently only supported on MI300X GPUs, and ROCm 7.0.2. 
and 6.4.4.
```

## ROCm-Finance components

````{list-table}
:header-rows: 1

* - Component
  - Version
  - Source

* - [CatBoost](https://rocm.docs.amd.com/projects/catboost-internal/en/latest/)
  - 1.2.8
  - {icon}`fa-brands fa-github fa-lg <https://github.com/ROCm/catboost>`

* - [XGBoost](https://rocm.docs.amd.com/projects/xgboost-internal/en/latest/)
  - 3.1.1
  - {icon}`fa-brands fa-github fa-lg <https://github.com/ROCm/xgboost>`

* - [LightGBM](https://rocm.docs.amd.com/projects/lightgbm-internal/en/latest/)
  - 4.6.0.99
  - {icon}`fa-brands fa-github fa-lg <https://github.com/ROCm/lightgbm>`

* - [ThunderGBM](https://rocm.docs.amd.com/projects/thundergbm-internal/en/latest/)
  - 0.3.16
  - {icon}`fa-brands fa-github fa-lg <https://github.com/ROCm/thundergbm>`
````
