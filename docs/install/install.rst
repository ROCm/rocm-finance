********************
Install ROCm Finance
********************

.. _install-rocm-dev-docker:

Install ROCm
============

To get up and running quickly, a prebuilt ROCm-enabled environment is
recommended. The easiest way is to use the offical ROCm Docker images from
Docker Hub. See :ref:`Docker images in the ROCm ecosystem
<rocm-install-on-linux:docker-rocm-images>` for more information.

1. Pull a ROCm dev Docker image with a supported configuration (see `Docker
   Hub <https://hub.docker.com/u/rocm?page=1&search=dev-ubuntu-2>`__ to browse
   available images). For example:

   .. tab-set::

      .. tab-item:: ROCm 7.0
         :sync: rocm7

         .. tab-set::

            .. tab-item:: Ubuntu 24.04
               :sync: ubuntu-24

               .. code-block:: shell

                  docker pull rocm/dev-ubuntu-24.04:7.0.2-complete

               See `rocm/dev-ubuntu-24.04:7.0.2-complete
               <https://hub.docker.com/layers/rocm/dev-ubuntu-24.04/7.0.2-complete/images/sha256-1f016cc06d83c615872d7464a9eeaa812b86d8e0512933a3be27bf3980ee5e06>`__
               on Docker Hub.

            .. tab-item:: Ubuntu 22.04
               :sync: ubuntu-22

               .. code-block:: shell

                  docker pull rocm/dev-ubuntu-22.04:7.0.2-complete

               See `rocm/dev-ubuntu-22.04:7.0.2-complete
               <https://hub.docker.com/layers/rocm/dev-ubuntu-22.04/7.0.2-complete/images/sha256-a60cffc2d079dbdc7a54948766e21793abdfeaa2ea95af60214f975a1ce51d06>`__
               on Docker Hub.

      .. tab-item:: ROCm 6.4
         :sync: rocm6

         .. tab-set::

            .. tab-item:: Ubuntu 24.04
               :sync: ubuntu-24

               .. code-block:: shell

                  docker pull rocm/dev-ubuntu-24.04:6.4.4-complete

               See `rocm/dev-ubuntu-24.04:6.4.4-complete
               <https://hub.docker.com/layers/rocm/dev-ubuntu-24.04/6.4.4-complete/images/sha256-31418ac10a3769a71eaef330c07280d1d999d7074621339b8f93c484c35f6078>`__
               on Docker Hub.

            .. tab-item:: Ubuntu 22.04
               :sync: ubuntu-22

               .. code-block:: shell

                  docker pull rocm/dev-ubuntu-22.04:6.4.4-complete

               See `rocm/dev-ubuntu-22.04:6.4.4-complete
               <https://hub.docker.com/layers/rocm/dev-ubuntu-22.04/6.4.4-complete/images/sha256-bdaa057ff7d6be321ada8d451aaab92777656557fa67985f27f2c98bd29c7a36>`__
               on Docker Hub.

2. Launch the Docker container.

   .. tab-set::

      .. tab-item:: ROCm 7.0
         :sync: rocm7

         .. tab-set::

            .. tab-item:: Ubuntu 24.04
               :sync: ubuntu-24

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

            .. tab-item:: Ubuntu 22.04
               :sync: ubuntu-22

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
                      rocm/dev-ubuntu-22.04:7.0.2-complete

      .. tab-item:: ROCm 6.4
         :sync: rocm6

         .. tab-set::

            .. tab-item:: Ubuntu 24.04
               :sync: ubuntu-24

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

            .. tab-item:: Ubuntu 22.04
               :sync: ubuntu-22

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
                      rocm/dev-ubuntu-22.04:6.4.4-complete

3. Install ROCm Finance libraries. See the following resources to get started:

   * `Install XGBoost <https://advanced-micro-devices-xgboost-internal--36.com.readthedocs.build/en/36/install/install.html>`__
   * `Install LightGBM <https://advanced-micro-devices-lightgbm-internal--2.com.readthedocs.build/en/2/install/install.html>`__
   * `Install ThunderGBM <https://advanced-micro-devices-thundergbm-internal--3.com.readthedocs.build/en/3/install/install.html>`__
