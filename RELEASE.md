---
myst:
  html_meta:
    "description lang=en": "AMD Finance 26.01 Release Notes"
    "keywords": "amd, rocm, gpu, finance, financial, sdk, gbm, credit, risk, forecast, simulation, trade, stock, optimize, portfolio, time, model"
---

# AMD Finance 26.01 release notes

This release introduces the popular XGBoost library to the AMD Finance
toolkit, enhancing machine learning capabilites for financial workloads.

## Release highlights

XGBoost is fully accelerated on AMD Instinct MI300X and MI325X GPUs (gfx942)
through ROCm 7.1.1, 7.0.2, or 6.4.4. This integration optimizes kernels,
improves memory management, and enables seamless multi-GPU scaling on supported
AMD GPUs.

Key benefits of this integration include:

* **Hardware acceleration:** Parallelizes split-finding on the GPU to deliver significant performance gains over CPU-only baselines.
* **Financial risk optimization:** Accelerates large-scale tasks such as credit risk scoring, fraud detection, and loan default modeling.
* **Compliance and precision:** Increases throughput while maintaining the native robustness (L1/L2 regularization) and missing value handling of XGBoost.

```{note}
AMD Finance libraries introduced in the 25.11 release, LightGBM and
ThunderGBM, are currently only supported on MI300X GPUs, and ROCm 7.0.2
and 6.4.4.
```

## Supported platforms

To learn about hardware and software environment requirements, see the
{doc}`/about/compatibility-matrix` and the {doc}`/install/prerequisites`.

## AMD Finance components

````{list-table}
:header-rows: 1

* - Component
  - Version
  - Source

* - [XGBoost](https://rocm.docs.amd.com/projects/xgboost/en/docs-26.01/)
  - 3.1.1
  - {icon}`fa-brands fa-github fa-lg <https://github.com/AMD-Ecosystem/xgboost>`

* - [LightGBM](https://rocm.docs.amd.com/projects/lightgbm/en/docs-26.01/)
  - 4.6.0.99
  - {icon}`fa-brands fa-github fa-lg <https://github.com/AMD-Ecosystem/lightgbm>`

* - [ThunderGBM](https://rocm.docs.amd.com/projects/thundergbm/en/docs-26.01/)
  - 0.3.16
  - {icon}`fa-brands fa-github fa-lg <https://github.com/AMD-Ecosystem/thundergbm>`

````
