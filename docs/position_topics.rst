.. _position_topics:


Position Topics
###############

Usually it would be ros-like to publish the positions of the crazyflies into the tf-Graph. 
For a motion_capture system this would not be an issue, because tracking at 20Hz there would be only 20 messages per second containing the transform for each crazyflie

However if the crazyflies are tracking themselves (lighthouse/ loco) each crazyflie publishes its own position at 20Hz on a seperate message. 
This would result in 400 messages per second for 20 crazyflies, which could overwhelm the tf-Graph.
For cpp nodes this rate is not an issue, but for python nodes this would result in a very high cpu load, making other usage of the tf-Graph difficult.

``/cf_positions`` Topic
======================

To mitigate this issue we decided not to use the tf-Graph for the positions. 
Instead we publish the positions of all crazyflies on a single topic ``/cf_positions``.
The message type for this topic is ``PoseStampedArray``. 
For Ros2 Jazzy and newer this type is part of `common_interfaces` for Humble the message needed to be defined in the ``crazyflie_interfaces``` package.


.. code-block:: 
    :caption: PoseStampedArray.msg

    std_msgs/Header header
    geometry_msgs/PoseStamped[] poses


The header is currently unused. 
For each pose we use the header.frame_id to specify the name of the crazyflie.
The position and orientation is then always in ``world`` coordinates.


Introspection
-------------

You can introspect the topic using the following command:

.. code-block:: bash

    ros2 topic echo /cf_positions

.. _rviz2-configuration:

Rviz2 Configuration
-------------------

Because the positions are not published into the tf-Graph, Rviz2 cannot visualize them by default. 
In order to do so the :doc:`crazyflies</crazyflies>` package provides a way to republish the positions as a `MarkerArray <https://docs.ros.org/en/humble/p/visualization_msgs/msg/MarkerArray.html>`_ and a `PoseArray <https://docs.ros.org/en/humble/p/geometry_msgs/msg/PoseArray.html>`_ msg.

You can simply add the following node to your launch file:

.. code-block:: python

    position_visualization = Node(
        package="crazyflies",
        executable="position_visualization",
        name="position_visualization",
    )

Then you can `add <https://docs.ros.org/en/humble/Tutorials/Intermediate/RViz/RViz-User-Guide/RViz-User-Guide.html#adding-a-new-display>`_ MarkerArray ``/cf_positions_marker`` and PoseArray ``/cf_positions_poses`` to Rviz2.
