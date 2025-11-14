***************************************
ROCm Finance installation prerequisites
***************************************

.. _system-requirements:

ROCm Finance supports the following ROCm software, operating system, and Python
versions. Ensure your system meets the required criteria before installing.

Supported hardware configurations
=================================

ROCm Finance supports AMD Instinct MI300X GPUs (gfx942).

Supported software configurations
=================================

The following table lists ROCm, Ubuntu, and Python versions supported by ROCm
Finance libraries.

.. list-table::
   :header-rows: 1

   * - ROCm version
     - Ubuntu version
     - Python version

   * - 7.0
     - 24.04
     - 3.12

   * - 6.4
     - 22.04
     - 3.10

Getting started
===============

Once you've verified system compatibility, proceed with installing ROCm Finance libraries.

1. First, install a supported ROCm version -- to get up and running quickly, it's recommended to
   start with a ROCm dev Docker. See :ref:`Install ROCm Finance <install-rocm-dev-docker>`.
   For other ROCm installation options, see :doc:`rocm-install-on-linux:index`.

2. Install ROCm Finance libraries. See the following resources to get started:

   * `Install XGBoost <https://advanced-micro-devices-xgboost-internal--36.com.readthedocs.build/en/36/install/install.html>`__
   * `Install LightGBM <https://advanced-micro-devices-lightgbm-internal--2.com.readthedocs.build/en/2/install/install.html>`__
   * `Install ThunderGBM <https://advanced-micro-devices-thundergbm-internal--3.com.readthedocs.build/en/3/install/install.html>`__
