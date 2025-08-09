.. _motion_capture:

.. toctree::
   :maxdepth: 100

Setting up Motion Capture
==========================


In the file `framework.launch.py <https://github.com/DynamicSwarms/ds-crazyflies/blob/master/src/crazyflies/launch/framework.launch.py>`_ you can configure the motion_capture system you are using. You can refer to this file: `motion_capture.cpp <https://github.com/DynamicSwarms/libmotioncapture/blob/main/src/motioncapture.cpp>`_ for your specific motion capture system.

Most importantly you need to configure ip and type of your motion capture system.

.. tabs::

   .. tab:: Vicon

      .. code-block:: python
 
         "type": "vicon",
         "hostname": "172.20.37.251",                 # your vicon ip
         "add_labeled_markers_to_pointcloud": True,   # wheter to exclude markers from tracked objects 

   .. tab:: OptiTrack
      
      .. code-block:: python
   
         "type": "optitrack",
         "hostname": "192.168.1.220",                 # your optitrack ip

Marker Configuration and Dynamics Configuration
***********************************************

In the  `framework.launch.py <https://github.com/DynamicSwarms/ds-crazyflies/blob/master/src/crazyflies/launch/framework.launch.py>`_ you can also pass your own version of `Tracker Configuration <https://github.com/DynamicSwarms/ros-objecttracker/blob/master/object_tracker/launch/tracker_config.yaml>`_.
This allows you can define the marker arrangement you placed on your crazyflie.

For most use cases the default configuration should work out of the box.

.. warning::

   Currently only single marker tracking is supported. The marker configuration is therefore not used and should be ignored.

Dynamics Configuration
-----------------------

In the dynamics configuration settings you can define the maximum dynamics of your crazyflie. Especially the maxVelocity fields define how far a marker is allowed to move each frame. For a slow tracking rate these parameters might need adjustment.
