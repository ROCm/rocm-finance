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

All ROCm-Finance libraries are supported on AMD Instinct™ MI300X GPUs.
XGBoost individually supports the additional hardware configurations of
AMD Instinct™ MI325X and MI355X GPUs (ROCm 7.2.3 only).

Before installing any component, verify that your system meets the hardware
and software prerequisites for each component, as outlined below. 
See the :ref:`finance-compat-matrix` page for more information.

Hardware requirements
---------------------------------------------------------------------------------------

The toolkit supports specific AMD GPU accelerators depending on the component:

- **XGBoost 3.2.0:** AMD Instinct™ MI355X (ROCm 7.2.3 only), MI325X, MI300X
- **LightGBM 4.6.0.99:** AMD Instinct™ MI300X
- **ThunderGBM 0.3.16:** AMD Instinct™ MI300X

Software requirements
----------------------------------------------------------------------------------------

ROCm version support varies by component:

- **XGBoost:** ROCm 7.2.3, 7.1.1, 7.0.2, 6.4.4
- **LightGBM:** ROCm 7.0.2, 6.4.4
- **ThunderGBM:** ROCm 7.0.2, 6.4.4

Get started
---------------------------------------------------------------------------------------

After confirming your system meets the supported hardware and software configurations, follow 
the steps outlined in :ref:`install-rocm-dev-docker`. For other ROCm installation options, 
see :doc:`rocm-install-on-linux:index`.
