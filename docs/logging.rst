.. _logging:

Logging
#######

The Crazyflie's logging feature streams variables from the firmware to ROS 2.
A **log block** groups variables that are published together at a chosen frequency.
Available variables depend on the firmware and backend. See the
`firmware logging reference <https://www.bitcraze.io/documentation/repository/crazyflie-firmware/master/api/logs/>`_
for variable names.

Creating and starting a log block
=================================

Connect a Crazyflie first, as described in :doc:`Usage </usage>`, and source
``install/setup.bash`` in each terminal. The examples below use Crazyflie ID 231;
replace ``/cf231`` with your Crazyflie's namespace.

Both the hardware backend and the lightweight simulation provide these services:

* ``/cf231/add_logging`` (``crazyflie_interfaces/srv/AddLogging``)
* ``/cf231/remove_logging`` (``crazyflie_interfaces/srv/RemoveLogging``)

``add_logging`` creates a block and starts publishing immediately. Its request is:

.. code-block:: text
    :caption: AddLogging.srv

    string topic_name
    int32 frequency
    string[] vars
    ---
    bool success

For example, log the battery voltage at 10 Hz:

.. code-block:: bash

    ros2 service call /cf231/add_logging crazyflie_interfaces/srv/AddLogging \
      "{topic_name: 'pm_log', frequency: 10, vars: ['pm.vbat']}"

Check that the response contains ``success: true``. The block publishes on
``/cf231/pm_log``. ``topic_name`` is the block name relative to the Crazyflie
namespace; use a unique name for each block and avoid built-in topics such as
``state``. Values follow the order of ``vars``.

``frequency`` is an integer in **Hz**, rather than a period in 10 ms units.
On hardware, the implementation converts it to a period in 10 ms steps, so some
requested frequencies are rounded. Use a positive frequency; 1, 2, 5, 10, 20, 50,
and 100 Hz map exactly to hardware periods. Never use zero, which causes division
by zero in the current implementation.

Hardware blocks must fit within the firmware's logging packet size and block
limits. The size depends on the firmware types of the requested variables, not
their ROS representation. Unknown variables and duplicate block names cause
creation to fail; check the Crazyflie node's output for details.

Receiving data
==============

Read the block's topic in another terminal:

.. code-block:: bash

    ros2 topic echo /cf231/pm_log

The message type is ``crazyflie_interfaces/msg/LogDataGeneric``:

.. code-block:: text
    :caption: LogDataGeneric.msg

    std_msgs/Header header
    uint32 timestamp
    float64[] values

``values`` contains the requested variables converted to ``float64``, in the
same order as ``vars``. For the example above, ``values[0]`` is ``pm.vbat``.
``timestamp`` represents the onboard timestamp in milliseconds when populated.

.. note::

    Timestamp population currently differs between publishers. Custom hardware
    log blocks leave both timestamp fields at their default values. Custom
    lightweight simulation blocks populate ``header.stamp``, but leave the
    onboard ``timestamp`` at zero. Do not assume both fields contain valid times.

Stopping and removing a log block
=================================

Remove the block with the same ``topic_name`` used to create it:

.. code-block:: bash

    ros2 service call /cf231/remove_logging crazyflie_interfaces/srv/RemoveLogging \
      "{topic_name: 'pm_log'}"

A successful response contains ``success: true``. This stops the block and
removes its ROS publisher. Removing an unknown block returns ``success: false``.
To change the variables or frequency, remove the block and create it again.
There are no separate start and stop topics in this interface.

Lightweight simulation
======================

The lightweight simulation supports the same add/remove services, with a limited
set of variables: ``pm.vbat``, ``pm.chargeCurrent``, ``pm.state``,
``stateEstimate.x``, ``stateEstimate.y``, ``stateEstimate.z``,
``stateEstimate.yaw``, and ``stateEstimate.qx/qy/qz/qw``.
The last notation refers to four separate variables, such as ``stateEstimate.qx``.

To print the available variables to the simulation node's console:

.. code-block:: bash

    ros2 topic pub --once /cf231/get_logging_toc_info std_msgs/msg/Empty '{}'

These instructions describe the hardware and lightweight simulation backends.
The deprecated Webots backend may expose a different logging interface.

Built-in state and position logging
===================================

Hardware automatically publishes a state block at 2 Hz on ``/cf231/state`` with
these values, in order:

#. `pm.vbat <https://www.bitcraze.io/documentation/repository/crazyflie-firmware/master/api/logs/#pmvbat>`_
#. `pm.chargeCurrent <https://www.bitcraze.io/documentation/repository/crazyflie-firmware/master/api/logs/#pmchargecurrent>`_
#. `pm.state <https://www.bitcraze.io/documentation/repository/crazyflie-firmware/master/api/logs/#pmstate>`_
#. `sys.canfly <https://www.bitcraze.io/documentation/repository/crazyflie-firmware/master/api/logs/#syscanfly>`_
#. `sys.isFlying <https://www.bitcraze.io/documentation/repository/crazyflie-firmware/master/api/logs/#sysisflying>`_
#. `sys.isTumbled <https://www.bitcraze.io/documentation/repository/crazyflie-firmware/master/api/logs/#sysistumbled>`_
#. `stateEstimate.yaw <https://www.bitcraze.io/documentation/repository/crazyflie-firmware/master/api/logs/#stateestimateyaw>`_ (degrees)

The lightweight simulation also publishes ``/cf231/state`` at 2 Hz, with the
first six values above. It does not include yaw in this built-in state message.

For hardware using internal position estimation (the default type), an
additional block logs position and orientation at 20 Hz. These are published on
``/cf_positions`` as ``crazyflie_interfaces/msg/PoseNamedArray``, rather than as a
custom log topic. See :doc:`Position Topics </position_topics>`.
