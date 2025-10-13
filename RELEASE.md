---
myst:
  html_meta:
    "description lang=en": "ROCm-Finance 26.01 Release Notes"
    "keywords": "amd, rocm, gpu, finance, financial, sdk, gbm, credit, risk, forecast, simulation, trade, stock, optimize, portfolio, time, model"
---

# AMD ROCm Finance 26.01 release notes

This release introduces the popular XGBoost library to the ROCm-Finance
toolkit, enhancing machine learning capabilites for financial workloads.

## Release highlights

XGBoost is now fully accelerated on AMD Instinct MI300X GPUs via ROCm 6.4.4 and
7.0.2, leveraging the CDNA 3 architecture and ROCm optimizations. The
integration features optimized kernels, improved memory management, and
seamless multi-GPU scaling.

Key benefits of this integration include:

* **Hardware acceleration:** Delivers significant speed-ups over CPU-only baselines in typical finance workloads by parallelizing split-finding on the GPU.
* **Financial risk optimization:** Accelerates large-scale tasks such as credit risk scoring, fraud detection, and loan default modeling.
* **Compliance and precision:** Maintains interpretability (L1/L2 regularization) and missing value handling inherent to XGBoost while increasing throughput.

## Supported platforms

To learn about hardware and software environment requirements, see the
{doc}`/about/compatibility-matrix` and the {doc}`/install/prerequisites`.

## ROCm-Finance components

````{list-table}
:header-rows: 1

* - Component
  - Version
  - Source

* - [XGBoost](https://rocm.docs.amd.com/projects/xgboost/en/latest/)
  - 3.1.1
  - {icon}`fa-brands fa-github fa-lg <https://github.com/ROCm/xgboost>`

* - [LightGBM](https://rocm.docs.amd.com/projects/lightgbm/en/latest/)
  - 4.6.0.99
  - {icon}`fa-brands fa-github fa-lg <https://github.com/ROCm/lightgbm>`

* - [ThunderGBM](https://rocm.docs.amd.com/projects/thundergbm/en/latest/)
  - 0.3.16
  - {icon}`fa-brands fa-github fa-lg <https://github.com/ROCm/thundergbm>`

````
