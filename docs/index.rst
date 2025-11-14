.. meta::
   :description: ROCm for the finance domain
   :keywords: amd, rocm, finance, gpu, instinct, sdk

***********************
AMD ROCm Finance Domain
***********************

The AMD ROCm platform is an open-source GPGPU computing ecosystem designed for
high-performance workloads. Within the ROCm ecosystem, the AMD ROCm Finance
Domain expansion SDK includes official, production‑ready support for three
industry‑leading Gradient Boosting Machine (GBM) libraries: XGBoost, LightGBM,
and ThunderGBM.

.. list-table::
   :header-rows: 1

   * - Feature
     - XGBoost
     - LightGBM
     - ThunderGBM

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

   * - Best for
     - General use
     - Large datasets
     - GPU-intensive tasks

   * - Primary finance use case
     - Credit-risk scoring, fraud detection, algorithmic trading
     - Portfolio optimization, time-series forecasting, market-microstructure analysis
     - High-frequency trading, large-scale scenario simulations

These libraries are fully accelerated on AMD GPUs via ROCm libraries,
leveraging the latest AMD GPU architectures. The integration includes optimized
kernels, memory‑management enhancements, and seamless multi‑GPU
scaling—delivering up to dramatic performance boosts over CPU‑only baselines in
typical finance workloads.

The ROCm Finance source code is hosted on GitHub at
`<https://github.com/ROCm/ROCm-Finance>`__.

ROCm Finance documentation is organized into the following categories:

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: Installation

      * :doc:`/install/install`

   .. grid-item-card:: Components

      * `XGBoost <https://advanced-micro-devices-xgboost-internal--36.com.readthedocs.build/en/36/>`__
      * `LightGBM <https://advanced-micro-devices-lightgbm-internal--2.com.readthedocs.build/en/2/>`__
      * `ThunderGBM <https://advanced-micro-devices-thundergbm-internal--3.com.readthedocs.build/en/3/>`__

   .. grid-item-card:: Related content

      * `Instinct docs <https://instinct.docs.amd.com/latest/>`__

   .. grid-item-card:: About

      * :doc:`License </about/license>`
