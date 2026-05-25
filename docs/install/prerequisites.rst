.. meta::
   :description: Prerequisites for installing ROCm-Finance toolkit libraries
   :keywords: amd, rocm, finance, financial, gpu, install, docker, libs, pip, package, lightgbm, thundergbm, setup, start

.. _system-requirements:

***************************************
ROCm-Finance installation prerequisites
***************************************

Before installing the ROCm-Finance libraries, verify that your system meets the
hardware and software prerequisites outlined here.

System requirements
======================================================================================

The ROCm-finance libraries are all supported on AMD Instinct MI300X GPUs.
Individually, XGBoost also supports additional hardware configurations.

Before installing any of the libraries, verify that your system meets the hardware
and software prerequisites for each component, as outlined below. 
See the :ref:`finance-compat-matrix` page for more information.

Hardware requirements
--------------------------------------------------------------------

The toolkit supports specific AMD GPU accelerators depending on the component:

- **XGBoost 3.2.0:** AMD Instinct MI300X, MI325X
- **LightGBM 4.6.0.99:** AMD Instinct MI300X
- **ThunderGBM 0.3.16:** AMD Instinct MI300X

Software dependencies
--------------------------------------------------------------------

ROCm version support varies by component:

- **XGBoost:** ROCm 7.2.3, 7.1.1, 7.0.2, 6.4.4
- **LightGBM:** ROCm 7.0.2, 6.4.4
- **ThunderGBM:** ROCm 7.0.2, 6.4.4

Getting started
======================================================================================

After confirming your system meets the supported hardware and software configurations, follow these steps
to install ROCm-Finance.

1. Install a supported ROCm version. To get up and running quickly, it's recommended to
   start with a ROCm dev Docker. See :ref:`Install ROCm-Finance <install-rocm-dev-docker>`.
   For other ROCm installation options, see :doc:`rocm-install-on-linux:index`.

2. Install ROCm-Finance libraries. Each library can have unique prerequisite and environment requirements. To avoid dependency
   conflicts and configuration errors, ensure each library is installed individually rather than
   through a unified installation process. The installation instructions for each library on ROCm can be found as follows:

   * `Install XGBoost <https://rocm.docs.amd.com/projects/xgboost/en/docs-26.05/install/install.html>`__
   * `Install LightGBM <https://rocm.docs.amd.com/projects/lightgbm/en/docs-25.11/install/install.html>`__
   * `Install ThunderGBM <https://rocm.docs.amd.com/projects/thundergbm/en/docs-25.11/install/install.html>`__
