.. meta::
   :description: Prerequisites for installing AMD Finance toolkit libraries
   :keywords: amd, rocm, finance, financial, gpu, install, docker, libs, pip, package, lightgbm, thundergbm, setup, start

***************************************
AMD Finance installation prerequisites
***************************************

.. _system-requirements:

Before installing the AMD Finance libraries, verify that your system meets the
hardware and software prerequisites outlined here.

Supported hardware configurations
=================================

See the :doc:`../about/compatibility-matrix` for an overview of hardware
support across AMD Finance releases.

.. list-table::
   :header-rows: 1

   * - ROCm Finance component
     - Supported AMD GPU

   * -
       * XGBoost 3.1.1
     -
       * AMD Instinct MI325X
       * AMD Instinct MI300X

   * -
       * LightGBM 4.6.0.99
       * ThunderGBM 4.6.0.99
     -
       * AMD Instinct MI300X

Supported software configurations
=================================

See the :doc:`../about/compatibility-matrix` for an overview of software
environment support across AMD Finance releases.

.. list-table::
   :header-rows: 1

   * - AMD Finance component
     - ROCm version
     - Ubuntu version
     - Python version

   * -
       * XGBoost 3.1.1
     -
       * 7.1.1
       * 7.0.2
       * 6.4.4
     - 24.04
     - 3.12

   * -
       * LightGBM 4.6.0.99
       * ThunderGBM 4.6.0.99
     -
       * 7.0.2
       * 6.4.4
     - 24.04
     - 3.12

Getting started
===============

After confirming your system meets the supported hardware and software configurations, follow these steps
to install AMD Finance.

1. Install a supported ROCm version. To get up and running quickly, it's recommended to
   start with a ROCm dev Docker. See :ref:`Install AMD Finance <install-rocm-dev-docker>`.
   For other ROCm installation options, see :doc:`rocm-install-on-linux:index`.

2. Install AMD Finance libraries. See the following resources to get started:

   * `Install XGBoost <https://rocm.docs.amd.com/projects/xgboost/en/docs-26.01/install/install.html>`__
   * `Install LightGBM <https://rocm.docs.amd.com/projects/lightgbm/en/docs-26.01/install/install.html>`__
   * `Install ThunderGBM <https://rocm.docs.amd.com/projects/thundergbm/en/docs-26.01/install/install.html>`__
