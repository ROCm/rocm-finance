.. meta::
   :description: AMD AMD Finance Toolkit
   :keywords: amd, rocm, finance, gpu, instinct, sdk, toolkit, library, fintech, gbm

******************************
AMD Finance documentation
******************************

Within the ROCm ecosystem, the AMD Finance toolkit includes
production‑ready support for industry‑leading Gradient Boosting Machine (GBM)
libraries for high-performance finance use cases:
`<https://github.com/microsoft/LightGBM>`__ and
`<https://github.com/Xtra-Computing/ThunderGBM>`__.

.. list-table::
   :header-rows: 1
   :stub-columns: 1

   * -
     - LightGBM
     - ThunderGBM

   * - Finance use cases
     -
       * Portfolio optimization
       * Time-series forecasting
       * Market-microstructure analysis
     -
       * High-frequency trading
       * Large-scale scenario simulations

   * - Best for
     - Large datasets
     - GPU-intensive tasks

   * - Tree growth strategy
     - Leaf-wise
     - Level-wise (GPU)

   * - Categorical feature handling
     - Manual + binning
     - Manual encoding

   * - Overfitting control
     - L1/L2 + sampling
     - Regularization

These libraries are accelerated on AMD Instinct GPUs through optimized ROCm
libraries, leveraging the latest AMD GPU architectures. ROCm enablement of
these libraries introduces optimized kernels, memory‑management enhancements,
and seamless multi‑GPU scaling, delivering performance gains over CPU-only
baselines in intensive workloads.

The AMD Finance source code is hosted on GitHub at
`https://github.com/AMD-Ecosystem/rocm-finance <https://github.com/AMD-Ecosystem/rocm-finance>`__.

AMD Finance documentation is organized into the following categories:

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: Install

      * :doc:`/install/prerequisites`
      * :doc:`/install/install`

   .. grid-item-card:: Components


      * `LightGBM <https://rocm.docs.amd.com/projects/lightgbm/en/docs-25.11/>`__
      * `ThunderGBM <https://rocm.docs.amd.com/projects/thundergbm/en/docs-25.11/>`__

   .. grid-item-card:: Tutorial

      * `Examples <https://github.com/AMD-Ecosystem/rocm-finance/tree/release/25.11/examples>`__
