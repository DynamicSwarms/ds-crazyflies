.. _docker:

Docker
######

In order to get started quickly with ROS 2 and ds-crazyflies we dockerised this project.
Therefore if you only want to have a quick peek at the project, you can use the provided Docker setup.
The image builds ROS 2 Lyrical and the lightweight simulation backend.

.. note::

    The image was built and the simulation tested on Ubuntu. The RQT state plugin
    also loaded in a headless test. The current Windows instructions have not yet
    been retested on Windows.

.. warning::

    Using the Docker setup with real hardware is neither tested nor recommended.
    The following instructions are for the lightweight simulation.

Ubuntu
======

1. Prerequisites
----------------

Install Docker Engine and the Docker Compose plugin. Make sure ``docker info``
works from your terminal. See the
`Docker Engine installation instructions <https://docs.docker.com/engine/install/ubuntu/>`_.

The provided Ubuntu Compose file uses X11 to display RQT. On a Wayland desktop
this requires XWayland. Check that ``DISPLAY`` is set and ``XAUTHORITY`` points
to your session's existing Xauthority file:

.. code-block:: bash

    echo "$DISPLAY"
    echo "$XAUTHORITY"
    test -f "$XAUTHORITY"

These values come from your desktop session; do not copy another user's paths.
If they are missing, configure X11/XWayland access before starting the container.

2. Build and start
------------------

Clone this repository and build from its root directory:

.. code-block:: bash

    git clone https://github.com/DynamicSwarms/ds-crazyflies.git
    cd ds-crazyflies
    docker compose -f docker/docker-compose.ubuntu_dev.yaml build
    docker compose -f docker/docker-compose.ubuntu_dev.yaml run --rm --name ds-crazyflies-ubuntu ros-dev-ubuntu

The last command opens a terminal inside the container. Keep it open while you
work. The Compose file mounts your local ``src`` directory into the container,
so source changes are shared with your PC. The image's compiled workspace is
already available under ``/ds/ds-crazyflies/install``.

3. Launch the simulation and RQT
--------------------------------

Inside the container, launch the framework:

.. code-block:: bash

    ros2 launch crazyflies framework.launch.py backend:=simulation

Open a second terminal on your PC and attach to the same container:

.. code-block:: bash

    docker exec -it ds-crazyflies-ubuntu bash

In this second container terminal, start RQT:

.. code-block:: bash

    rqt --force-discover

Follow :doc:`Usage </usage>` to add a simulated Crazyflie and use the control panel.
When finished, stop RQT and the framework with Ctrl+C, then exit the container's
original shell. The ``--rm`` option removes the container when it exits.

Windows
=======

1. Docker Desktop and display setup
-----------------------------------

Install `Docker Desktop <https://docs.docker.com/desktop/setup/install/windows-install/>`_
and use Linux containers with the
`WSL 2 backend <https://docs.docker.com/desktop/features/wsl/>`_.
Make sure ``docker info`` works from PowerShell.

Install and launch MobaXterm:

https://mobaxterm.mobatek.net/download.html

.. warning::

    We also tried VcXsrv with our setup. This did not work!

If you need Webots, the Windows Compose file
``docker/docker-compose.windows_dev.yaml`` with the NVIDIA GPU settings is still
available. The commands below use ``docker run`` for the lightweight simulation.

2. Build and start
------------------

From PowerShell, clone this repository and build the same image used on Ubuntu:

.. code-block:: powershell

    git clone https://github.com/DynamicSwarms/ds-crazyflies.git
    cd ds-crazyflies
    docker build --build-arg ROS_DISTRO=lyrical -f docker/Dockerfile -t ds-crazyflies:dev .
    docker run --rm -it --name ds-crazyflies-windows -e DISPLAY=host.docker.internal:0.0 -e QT_X11_NO_MITSHM=1 ds-crazyflies:dev bash

This opens a Linux shell inside the container. It uses the source files copied
during the build; it does not mount your Windows checkout.

3. Launch the simulation and RQT
--------------------------------

Inside the container, launch the framework:

.. code-block:: bash

    ros2 launch crazyflies framework.launch.py backend:=simulation

In a second PowerShell terminal, attach to the same container:

.. code-block:: powershell

    docker exec -it ds-crazyflies-windows bash

Inside this second container terminal, start RQT:

.. code-block:: bash

    rqt --force-discover

Follow :doc:`Usage </usage>` to connect a simulated Crazyflie. The framework and
RQT run inside the same container, so host networking is not needed for this
workflow.

When finished, stop RQT and the framework with Ctrl+C, then exit the original
container shell. The container is removed automatically.
