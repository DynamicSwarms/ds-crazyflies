.. _diagnostics:

Diagnostics & Troubleshooting
#############################

Use diagnostics to inspect radio communication, Crazyflie initialization, and
external tracking while the framework is running. Components publish
``diagnostic_msgs/msg/DiagnosticArray`` messages on ``/diagnostics``.
Simulations currently do not provide diagnostics.

Install the diagnostics viewer
==============================

Install **RQT Runtime Monitor** for ROS 2 Lyrical:

.. code-block:: bash

   sudo apt update
   sudo apt install ros-lyrical-rqt-runtime-monitor

.. note::

   You probably need to apply this Qt6 compatibility fix on Lyrical. The
   installed viewer may report ``AttributeError: type object 'Qt' has no
   attribute 'UserRole'`` and accumulate duplicate rows, making RQT laggy.

   Close RQT first, then back up and patch the installed viewer:

   .. code-block:: bash

      monitor_file=/opt/ros/lyrical/lib/python3.14/site-packages/rqt_runtime_monitor/runtime_monitor_widget.py

      sudo cp -n "$monitor_file" "${monitor_file}.before-qt6-fix"
      sudo sed -i \
        -e 's/Qt\.UserRole/Qt.ItemDataRole.UserRole/g' \
        -e 's/Qt\.AscendingOrder/Qt.SortOrder.AscendingOrder/g' \
        -e 's/Qt\.Key_Delete/Qt.Key.Key_Delete/g' \
        "$monitor_file"

   Restart RQT afterwards. An apt upgrade or reinstall may overwrite this
   patch; reapply it if the same error returns.

You can then add the **Runtime Monitor** plugin to RQT by selecting **Plugins → Robot Tools → Runtime Monitor**.. 

You might need to run ``rqt --force-discover``.

What to look at
===============

* **Crazyradio:** Radio/CRTP quality, RSSI, outgoing packet age, delivery delay,
  and queue size.
* **Hardware gateway:** Configuring/ready/removing counts, pending requests,
  and processing time.
* **Motion capture:** Connection state, received frames, marker/body counts,
  and SDK latency.
* **Object tracker:** Input rate, usable frame age, observation age,
  and tracking losses.

Inspect from the terminal
=========================

.. code-block:: bash

   ros2 topic echo /diagnostics
   
For per-Crazyflie radio quality and RSSI:

.. code-block:: bash

   ros2 topic echo /crazyradio/link_qualities


Radio log files
===============

With the default ``log_enabled=true``, each radio writes beneath the ROS log
directory (normally ``~/.ros/log``):

.. code-block:: text

   crazyradio/<channel>/packets.log
   crazyradio/<channel>/radio.log

``packets.log`` records CRTP requests and responses. For USB radios,
``radio.log`` records transfer outcomes, retries, and RSSI. Matching transfer IDs
allow the two files to be compared. 
