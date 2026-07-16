---
myst:
  html_meta:
    "description lang=en": "ROCm-Finance 25.11 Release Notes"
    "keywords": "amd, rocm, gpu, finance, financial, sdk, gbm, credit, risk, forecast, simulation, trade, stock, optimize, portfolio, time, model"
---

# AMD Finance 25.11 release notes

This is the initial release of the AMD Finance toolkit, providing
production-ready support for GPU-accelerated Gradient Boosting Machine (GBM)
libraries on ROCm 7.0 and 6.4.

## Release highlights

This release introduces two libraries with ROCm support.

- **LightGBM** is an open-source gradient boosting framework developed by
  Microsoft specializing in tree-based learning algorithms for supervised
  machine learning tasks like classification, regression, and ranking.
- **ThunderGBM** is an open-source library developed by Xtra-Computing that
  accelerates Gradient Boosted Decision Trees (GBDTs) and Random Forests
  using GPUs, enabling high-performance machine learning for large-scale
  datasets.

See [AMD Finance components](#amd-finance-components) for details.

## Supported platforms

To learn about hardware and software environment requirements, see the
{doc}`/about/compatibility-matrix` and the {doc}`/install/prerequisites`.

## AMD Finance components

````{list-table}
:header-rows: 1

* - Component
  - Version
  - Source

* - [LightGBM](https://rocm.docs.amd.com/projects/lightgbm/en/docs-25.11/)
  - 4.6.0.99
  - {icon}`fa-brands fa-github fa-lg <https://github.com/AMD-Ecosystem/lightgbm>`

* - [ThunderGBM](https://rocm.docs.amd.com/projects/thundergbm/en/docs-25.11/)
  - 0.3.16
  - {icon}`fa-brands fa-github fa-lg <https://github.com/AMD-Ecosystem/thundergbm>`

````
