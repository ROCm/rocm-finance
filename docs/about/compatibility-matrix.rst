.. meta::
   :description: AMD ROCm-Finance compatibility information
   :keywords: amd, rocm, finance, gpu, instinct, sdk, system, requirements, compatibility, support, version, upstream, library, env

*********************************
ROCm-Finance compatibility matrix
*********************************

This table provides system and library compatibility information for the
ROCm-Finance libraries.

.. list-table::
   :header-rows: 1

   * - ROCm-Finance version
     - Components
     - AMD Instinct GPU
     - ROCm version
     - Operating system
     - Python version

   * - 26.02 [#2602-footnote]_
     -
       * CatBoost 1.2.8
       * XGBoost 3.1.1
       * LightGBM 4.6.0.99
       * ThunderGBM 0.3.16
     -
       * MI325X (XGBoost only) [#2601-footnote]_
       * MI300X
     -
       * 7.1.1 (XGBoost only) [#2601-footnote]_
       * 7.0.2
       * 6.4.4
     - Ubuntu 24.04
     - 3.12

   * - - `26.01 <https://rocm.docs.amd.com/projects/rocm-finance/en/docs-26.01/>`__ [#2601-footnote]_
     -
       * XGBoost 3.1.1
       * LightGBM 4.6.0.99
       * ThunderGBM 0.3.16
     -
       * MI325X (XGBoost only) [#2601-footnote]_
       * MI300X
     -
       * 7.1.1 (XGBoost only) [#2601-footnote]_
       * 7.0.2
       * 6.4.4
     - Ubuntu 24.04
     - 3.12

   * - `25.11 <https://rocm.docs.amd.com/projects/rocm-finance/en/docs-25.11/>`__
     -
       * LightGBM 4.6.0.99
       * ThunderGBM 0.3.16
     - MI300X
     -
       * 7.0.2
       * 6.4.4
     - Ubuntu 24.04
     - 3.12

.. rubric:: Footnotes

.. [#2602-footnote] Only CatBoost and XGBoost are supported with ROCm 7.1.1.
   LightGBM and ThunderGBM are currently only supported on MI300X GPUs, and
   ROCm 7.0.2 and 6.4.4.

.. [#2601-footnote] Only XGBoost is supported with ROCm 7.1.1.
   LightGBM and ThunderGBM are currently only supported on MI300X GPUs, and
   ROCm 7.0.2 and 6.4.4.

.. seealso::

   See :doc:`/install/prerequisites` for an overview of supported hardware and
   software configurations.
