.. meta::
   :description: Prerequisites for installing ROCm Finance Expansion SDK libraries
   :keywords: amd, rocm, finance, financial, gpu, install, docker, libs, pip, package, lightgbm, thundergbm, setup, start

***************************************
ROCm Finance installation prerequisites
***************************************

.. _system-requirements:

Before installing ROCm Finance libraries, verify that your system meets the
hardware and software prerequisites outlined here.

Supported hardware configurations
=================================

ROCm Finance supports AMD Instinct MI300X GPUs.

Supported software configurations
=================================

The following table lists ROCm, Ubuntu, and Python versions supported by ROCm
Finance libraries.

.. list-table::
   :header-rows: 1

   * - ROCm version
     - Ubuntu version
     - Python version

   * - 7.0.2
     - 24.04
     - 3.12

   * - 6.4.4
     - 22.04
     - 3.10

Getting started
===============

After confirming your system meets the supported hardware and software configurations, follow these steps
to install ROCm Finance.

1. Install a supported ROCm version. To get up and running quickly, it's recommended to
   start with a ROCm dev Docker. See :ref:`Install ROCm Finance <install-rocm-dev-docker>`.
   For other ROCm installation options, see :doc:`rocm-install-on-linux:index`.

2. Install ROCm Finance libraries. See the following resources to get started:

   * `Install LightGBM <https://rocm.docs.amd.com/projects/lightgbm-internal/en/latest/install/install.html>`__
   * `Install ThunderGBM <https://rocm.docs.amd.com/projects/thundergbm-internal/en/latest/install/install.html>`__
