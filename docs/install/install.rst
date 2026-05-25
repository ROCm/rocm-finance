.. meta::
   :description: Install ROCm-Finance SDK libraries
   :keywords: amd, rocm, finance, financial, gpu, install, docker, libs, pip, package, lightgbm, thundergbm, setup, quick, start, xgboost

********************
Install ROCm-Finance
********************

This page provides brief guidance and recommendations on setting up
a ROCm-enabled environment for financial computing workloads. This includes
pulling and running prebuilt ROCm Docker images for supported Ubuntu versions
and installing ROCm-Finance libraries such as XGBoost, LightGBM, and
ThunderGBM.

.. _install-rocm-dev-docker:

Install ROCm
======================================================================================

To get up and running quickly, a prebuilt ROCm-enabled container is
recommended. The easiest way is to use the offical ROCm Docker images from
Docker Hub. See :ref:`Docker images in the ROCm ecosystem
<rocm-install-on-linux:docker-rocm-images>` for more information.

1. Pull a ROCm dev Docker image with a supported configuration (see `Docker
   Hub <https://hub.docker.com/u/rocm?page=1&search=dev-ubuntu-2>`__ to browse
   available images). For example:

   .. tab-set::

      .. tab-item:: ROCm 7.0.2
         :sync: rocm7

         .. code-block:: shell

            docker pull rocm/dev-ubuntu-24.04:7.0.2-complete

         See `rocm/dev-ubuntu-24.04:7.0.2-complete
         <https://hub.docker.com/layers/rocm/dev-ubuntu-24.04/7.0.2-complete/images/sha256-1f016cc06d83c615872d7464a9eeaa812b86d8e0512933a3be27bf3980ee5e06>`__
         on Docker Hub.

      .. tab-item:: ROCm 6.4.4
         :sync: rocm6

         .. code-block:: shell

            docker pull rocm/dev-ubuntu-24.04:6.4.4-complete

         See `rocm/dev-ubuntu-24.04:6.4.4-complete
         <https://hub.docker.com/layers/rocm/dev-ubuntu-24.04/6.4.4-complete/images/sha256-31418ac10a3769a71eaef330c07280d1d999d7074621339b8f93c484c35f6078>`__
         on Docker Hub.

2. Launch the Docker container.

   .. tab-set::

      .. tab-item:: ROCm 7.0.2
         :sync: rocm7

         .. code-block:: shell

            docker run -it \
                --cap-add=SYS_PTRACE \
                --ipc=host \
                --privileged=true \
                --shm-size=128GB \
                --network=host \
                --device=/dev/kfd \
                --device=/dev/dri \
                --group-add video \
                -v $HOME:$HOME \
                --name rocm7 \
                rocm/dev-ubuntu-24.04:7.0.2-complete

      .. tab-item:: ROCm 6.4.4
         :sync: rocm6

         .. code-block:: shell

            docker run -it \
                --cap-add=SYS_PTRACE \
                --ipc=host \
                --privileged=true \
                --shm-size=128GB \
                --network=host \
                --device=/dev/kfd \
                --device=/dev/dri \
                --group-add video \
                -v $HOME:$HOME \
                --name rocm6 \
                rocm/dev-ubuntu-24.04:6.4.4-complete

Install ROCm-Finance libraries
======================================================================================

Each library has distinct prerequisite and environment requirements. To avoid dependency
conflicts and configuration errors, ensure each library is installed individually rather than
through a unified installation process.

The installation instructions for each library on ROCm can be found as follows:

* `Install XGBoost <https://rocm.docs.amd.com/projects/xgboost/en/latest/install/install.html>`__
* `Install LightGBM <https://rocm.docs.amd.com/projects/lightgbm/en/latest/install/install.html>`__
* `Install ThunderGBM <https://rocm.docs.amd.com/projects/thundergbm/en/latest/install/install.html>`__
