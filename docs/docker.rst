.. _docker:

Docker
######

In order to get started quickly with Ros2 and ds-crazyflies we dockerised this project.
Therefore if you only want to have a quick peek at the project, you can use the provided Docker setup.
With the container you will be able to run webots with a single crazyflie. 

.. note::

    The Docker setup described here was created for Windows 11 with a nvidia GPU and `DockerDesktop <https://docs.docker.com/desktop/>`_.
    If you do have a different setup, you may need to adjust the docker-compose file etc.

.. warning:: 

    Using the docker setup with real hardware is neither tested nor recommended.
    It should only be used with the Webots simulation. 

1. Docker-Desktop Settings
==========================

Inside DockerDesktop go to Settings -> Docker Engine and add the following configuration:

.. code-block:: yaml

     "runtimes": {
        "nvidia": {
        "path": "/usr/bin/nvidia-container-runtime",
        "runtimeArgs": []
        }
    }



2. MobaXterm
============

Install and launch MobaXterm: 

https://mobaxterm.mobatek.net/download.html

! We also tried VcXsrv with our setup. This did not work !

3. Building the Image
=====================

#. Clone this repo to your local machine:

   .. code-block:: bash

      git clone https://github.com/DynamicSwarms/ds-crazyflies.git   

#. Run the services in `docker/docker-compose.windows_dev.yaml`

    We used VSCode with the following extensions:

        * `Docker <https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker>`_
        * `Container Tools <https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-containers>`_
        * `Dev Containers <https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers>`_
 
    With this setup open the cloned `ds-crazyflies` folder with VSCode. 
    Open the docker-compose file and a button appears to run the service. 

4. Usage
========

#. Run the `ros-dev-windows` service. 

    This will start the container. (See :doc:`Usage</usage>`).
    

#. You can now attach a terminal to the running container.

    With the VSCode extension you can do this by clicking on the container in the Docker view and selecting `Attach Shell`.
    Or you can `Attach Visual Studio Code` and then open a terminal in the fresh VSCode window. 

#. Open Webots from this terminal.
    There are sometimes issues when launching webots. We had better luck testing with the `--batch` flag.

    .. code::

        webots /ds/crazywebotsworld/worlds/crazyflie.wbt --batch

    This also closes any pop ups that may appear when launching webots the first time.

#. You can now use the ROS 2 CLI and get comfortable with the framework:  

    - Launch the frame work:

    .. code-block:: bash

        ros2 launch crazyflies framework.launch.py 

    - Use rqt to add and control a crazyflie (see :doc:`Usage</usage>`):
    
    .. code-block:: bash

        rqt --force-discover   

