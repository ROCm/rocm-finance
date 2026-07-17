.. meta::
   :description: AMD Finance compatibility information
   :keywords: amd, rocm, finance, gpu, instinct, sdk, system, requirements, compatibility, support, version, upstream, library, env

.. _finance-compat-matrix:

**************************************************************************************
AMD Finance compatibility matrix
**************************************************************************************

Use the following matrix to view the AMD Finance compatibility and system requirements across releases:

.. role:: version-start

.. table::
   :width: 65%
   :widths: 20 10 16 12 6 8
   :align: left
   :class: compat-matrix format-big-table

   +------------------------+----------------------------------------------------+------------------+--------------+--------+----------------+
   |  AMD Finance version   |                  Component                         | AMD Instinct GPU | ROCm version | Ubuntu |    Python      |
   +========================+====================================================+==================+==============+========+================+
   | :version-start:`26.05` | `XGBoost 3.2.0                                     | MI355X [#f1]_,   | 7.2.3,       | 24.04  | 3.12,          |
   |                        | <https://rocm.docs.amd.com/projects/               | MI325X,          | 7.1.1,       |        | 3.11,          |
   |                        | xgboost-internal/en/docs-26.05/>`__                | MI300X           | 7.0.2        |        | 3.10           |
   +------------------------+----------------------------------------------------+------------------+--------------+--------+----------------+
   | :version-start:`26.01` | `XGBoost 3.1.1                                     | MI325X [#f1]_,   | 7.1.1,       | 24.04  | 3.12           |
   |                        | <https://rocm.docs.amd.com/projects/               | MI300X           | 7.0.2,       |        |                |
   |                        | xgboost/en/docs-26.01/>`__                         |                  | 6.4.4        |        |                |
   +------------------------+----------------------------------------------------+------------------+--------------+--------+----------------+
   | :version-start:`25.11` | `LightGBM 4.6.0.99                                 | MI300X [#f2]_    | 7.0.2,       | 24.04  | 3.12           |
   |                        | <https://rocm.docs.amd.com/projects/               |                  | 6.4.4        |        |                |
   |                        | lightgbm/en/docs-25.11/>`__                        |                  |              |        |                |
   +                        +----------------------------------------------------+------------------+--------------+--------+----------------+
   |                        | `ThunderGBM 0.3.16                                 | MI300X [#f2]_    | 7.0.2,       | 24.04  | 3.12           |
   |                        | <https://rocm.docs.amd.com/projects/               |                  | 6.4.4        |        |                |
   |                        | thundergbm/en/docs-25.11/>`__                      |                  |              |        |                |
   +------------------------+----------------------------------------------------+------------------+--------------+--------+----------------+


.. rubric:: Footnotes

.. [#f1] Only XGBoost is supported with ROCm 7.2.3 and 7.1.1,
   with support for MI355X (ROCm 7.2.3 only) and MI325X GPUs.

.. [#f2] LightGBM and ThunderGBM are currently only supported on MI300X GPUs, with
   ROCm 7.0.2 and 6.4.4.


.. seealso::

   See :doc:`/install/prerequisites` for an overview of supported hardware and
   software configurations.
