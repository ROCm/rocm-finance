# ROCm Finance 25.11 release notes

This is the initial release of the AMD ROCm Finance Domain SDK, providing
production-ready support for GPU-accelerated Gradient Boosting Machine (GBM)
libraries on ROCm 6.4 and 7.0.

## Release highlights

This release introduces three ROCm-enabled libraries.

- **XGBoost** -- Fully optimized for AMD GPUs with support for credit-risk
  scoring, fraud detection, and algorithmic trading workloads.
- **LightGBM** -- GPU-accelerated implementation for portfolio optimization,
  time-series forecasting, and market microstructure analysis.
- **ThunderGBM** -- Native GPU execution for high-frequency trading and
  large-scale scenario simulations.

See [ROCm Finance components](#rocm-finance-components) for details.

### High-level features

- Full GPU acceleration on AMD Instinct MI300X (CDNA 3 architecture)
- Optimized kernels and memory management enhancements
- Seamless multi-GPU scaling support
- Comprehensive installation documentation for all three ROCm-enabled GBM libraries
- Example implementations for financial use cases


## Supported platforms

- **Hardware** -- AMD Instinct MI300X GPUs (gfx942)
- **Linux distribution** -- Ubuntu 24.04 and 22.04
- **ROCm version** -- 7.0 and 6.4
- **Python version** -- 3.12 and 3.10

## ROCm Finance components

````{list-table}
:header-rows: 1

* - Component
  - Version
  - Source

* - [XGBoost](https://advanced-micro-devices-xgboost-internal--36.com.readthedocs.build/en/36/)
  - 3.11
  - {icon}`fa-brands fa-github fa-lg <https://github.com/ROCm/xgboost>`

* - [LightGBM](https://advanced-micro-devices-lightgbm-internal--2.com.readthedocs.build/en/2/)
  - 4.6.0.99
  - {icon}`fa-brands fa-github fa-lg <https://github.com/ROCm/lightgbm>`

* - [ThunderGBM](https://advanced-micro-devices-thundergbm-internal--3.com.readthedocs.build/en/3/)
  - 0.3.16
  - {icon}`fa-brands fa-github fa-lg <https://github.com/ROCm/thundergbm>`

````
