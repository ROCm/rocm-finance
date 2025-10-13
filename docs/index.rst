.. meta::
   :description: AMD ROCm Finance Expansion SDK
   :keywords: amd, rocm, finance, gpu, instinct, sdk, expansion, toolkit, library, fintech, gbm

****************
AMD ROCm Finance
****************

The AMD ROCm software stack is an open-source high performance GPU computing
ecosystem designed for high-performance workloads. Within the ROCm ecosystem,
the AMD ROCm Finance expansion toolkit includes production‑ready support for
industry‑leading Gradient Boosting Machine (GBM) libraries: LightGBM and
ThunderGBM.

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

These libraries are accelerated on AMD GPUs through optimized ROCm libraries
leveraging the latest AMD GPU architectures. ROCm enablement of these libraries
introduces optimized kernels, memory‑management enhancements, and seamless
multi‑GPU scaling, delivering performance gains over CPU-only baselines in
intensive workloads.

The ROCm Finance source code is hosted on GitHub at
`<https://github.com/ROCm-Finance/ROCm-Finance>`__.

ROCm Finance documentation is organized into the following categories:

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: Install

      * :doc:`/install/prerequisites`
      * :doc:`/install/install`

   .. grid-item-card:: Components

      * `LightGBM <https://rocm.docs.amd.com/projects/lightgbm-internal/en/latest/>`__
      * `ThunderGBM <https://rocm.docs.amd.com/projects/thundergbm-internal/en/latest/>`__

   .. grid-item-card:: Tutorial

      * `Examples <https://github.com/AMD-AIOSS/rocm-finance/tree/main/examples>`__
