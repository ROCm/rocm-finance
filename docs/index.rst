.. meta::
   :description: AMD ROCm-Finance Toolkit
   :keywords: amd, rocm, finance, gpu, instinct, sdk, toolkit, library, fintech, gbm

******************************
AMD ROCm Finance documentation
******************************

Within the ROCm ecosystem, the AMD ROCm Finance toolkit (ROCm-Finance) includes
production‑ready support for industry‑leading Gradient Boosting Machine (GBM)
libraries for high-performance finance use cases:

.. list-table::
   :header-rows: 1
   :stub-columns: 1

   * -
     - `XGBoost <https://rocm.docs.amd.com/projects/xgboost-internal>`__
     - `LightGBM <https://rocm.docs.amd.com/projects/lightgbm>`__
     - `ThunderGBM <https://rocm.docs.amd.com/projects/thundergbm>`__

   * - Finance use cases
     -
       * Credit risk scoring
       * Fraud detection
       * Algorithmic trading
     -
       * Portfolio optimization
       * Time-series forecasting
       * Market-microstructure analysis
     -
       * High-frequency trading
       * Large-scale scenario simulations

   * - Best for
     - General use
     - Large datasets
     - GPU-intensive tasks

   * - Tree growth strategy
     - Level-wise
     - Leaf-wise
     - Level-wise (GPU)

   * - Categorical feature handling
     - Manual encoding
     - Manual + binning
     - Manual encoding

   * - Overfitting control
     - L1/L2 + early stop
     - L1/L2 + sampling
     - Regularization

These components are accelerated on AMD Instinct GPUs through optimized ROCm
libraries, leveraging the latest AMD GPU architectures. ROCm enablement of
these libraries introduces optimized kernels, memory‑management enhancements,
and seamless multi‑GPU scaling, delivering performance gains over CPU-only
baselines in intensive workloads.

The ROCm-Finance source code is hosted on GitHub at
`<https://github.com/ROCm/ROCm-Finance>`__.

ROCm-Finance documentation is organized into the following categories:

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: Install

      * :doc:`/install/prerequisites`
      * :doc:`/install/install`

   .. grid-item-card:: Components

      * `XGBoost <https://rocm.docs.amd.com/projects/xgboost/en/latest/>`__
      * `LightGBM <https://rocm.docs.amd.com/projects/lightgbm/en/latest/>`__
      * `ThunderGBM <https://rocm.docs.amd.com/projects/thundergbm/en/latest/>`__

   .. grid-item-card:: Tutorial

      * `Examples <https://github.com/ROCm/rocm-finance/tree/main/examples>`__
