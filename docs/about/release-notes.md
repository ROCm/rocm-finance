---
myst:
  html_meta:
    "description lang=en": "ROCm Finance SDK 25.11 Release Notes"
    "keywords": "amd, rocm, gpu, finance, financial, sdk, gbm, credit, risk, forecast, simulation, trade, stock, optimize, portfolio, time, model"
---

# ROCm Finance 25.11 release notes

This is the initial release of the AMD ROCm Finance Domain SDK, providing
production-ready support for GPU-accelerated Gradient Boosting Machine (GBM)
libraries on ROCm 7.0 and 6.4.

## Release highlights

This release introduces two libraries for financial use cases with ROCm
support.

- **LightGBM** -- GPU-accelerated implementation for portfolio optimization,
  time-series forecasting, and market microstructure analysis.
- **ThunderGBM** -- Native GPU execution for high-frequency trading and
  large-scale scenario simulations.

See [ROCm Finance components](#rocm-finance-components) for details.

## Supported platforms

To learn about hardware and software environment requirements, see the
{doc}`/about/compatibility-matrix` and the {doc}`/install/prerequisites`.

## ROCm Finance components

````{list-table}
:header-rows: 1

* - Component
  - Version
  - Source

* - [LightGBM](https://rocm.docs.amd.com/projects/lightgbm-internal/en/latest/)
  - 4.6.0.99
  - {icon}`fa-brands fa-github fa-lg <https://github.com/ROCm/lightgbm>`

* - [ThunderGBM](https://rocm.docs.amd.com/projects/thundergbm-internal/en/latest/)
  - 0.3.16
  - {icon}`fa-brands fa-github fa-lg <https://github.com/ROCm/thundergbm>`

````
