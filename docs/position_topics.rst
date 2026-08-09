.. _position_topics:


Position Topics
###############

Usually it would be ros-like to publish the positions of the crazyflies into the tf-Graph. 
For a motion_capture system this would not be an issue, because tracking at 20Hz there would be only 20 messages per second containing the transform for each crazyflie.

However if the crazyflies are tracking themselves (lighthouse/ loco) each crazyflie publishes its own position at 20Hz on a seperate message. 
This would result in 400 messages per second for 20 crazyflies, which could overwhelm the tf-Graph.
For cpp nodes this rate is not an issue, but for python nodes this would result in a very high cpu load, making other usage of the tf-Graph difficult.

``/cf_positions`` Topic
======================

To mitigate this issue we decided not to use the tf-Graph for the positions. 
Instead we publish the positions of all crazyflies on a single topic ``/cf_positions``.
The message type for this topic is ``PoseNamedArray``, define in the ``crazyflie_interfaces`` package.


.. code-block:: 
    :caption: PoseNamedArray.msg  

    std_msgs/Header header
    geometry_msgs/PoseNamed[] poses

.. code-block:: 
    :caption: PoseNamed.msg  

    string name
    bool rotation_valid true
    std_msgs/Header header
    geometry_msgs/Pose pose


The header contains the timestamp of the message.
Then there is a PoseNamed for each crazyflie.
The name-field contains a name in the format ``cf<id>`` where <id> is the id of the crazyflie.
The header contains the frame_id in which the pose is expressed.
Then there is a Pose which contains the position and orientation of the crazyflie.
If the orientation data in the pose is not valid, the rotation_valid field is set to false. 
This is the case for the motion_capture systems which rely on single marker tracking, and thus cannot provide orientation data.


Introspection
-------------

You can introspect the topic using the following command:

.. code-block:: bash

    ros2 topic echo /cf_positions

.. _rviz2-configuration:

Rviz2 Configuration
-------------------

Rviz2 cannot visualize the PoseNamedArray message type by default.
Therefore a custom rviz2 display was created in the `crazyflie_interfaces_rviz_displays <https://github.com/DynamicSwarms/crazyflie_interfaces_rviz_displays>`_ package.
Then you can `add <https://docs.ros.org/en/lyrical/Tutorials/Intermediate/RViz/RViz-User-Guide/RViz-User-Guide.html#adding-a-new-display>`_ this display to your rviz2 configuration and select the ``/cf_positions`` topic.
Poses of crazyflies with valid orientation data will be visualized as arrows, while poses of crazyflies with invalid orientation data will be visualized as flattened spheres.