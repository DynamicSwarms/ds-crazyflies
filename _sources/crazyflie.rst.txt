.. _crazyflie:

.. toctree:: 
   :maxdepth: 100

Crazyflie
==========

This library was tested with the `Crazyflie 2.1 <https://www.bitcraze.io/products/crazyflie-2-1-plus/>`_ but not yet with the `Crazyflie Bushless <https://www.bitcraze.io/products/crazyflie-2-1-brushless/>`_.

#. Checkout this guide if it is your first time using a Crazyflie: `Getting started with the Crazyflie 2.1 <https://www.bitcraze.io/documentation/tutorials/getting-started-with-crazyflie-2-x/>`_.

#. Flash the Crazyflie firmware: This library was tested with version 2022.09 and 2025.02 of the Crazyflie firmware. Checkout `this guide <https://www.bitcraze.io/documentation/repository/crazyflie-clients-python/master/userguides/userguide_client/#firmware-upgrade>`_ to upgrade your Crazyflie firmware.

#. Use `these instructions <https://www.bitcraze.io/documentation/repository/crazyflie-clients-python/master/userguides/userguide_client/#firmware-configuration>`_ to configure a unique **Id** and a **Channel** for each crazyflie.

IDs and Channels
----------------

Each Crazyflie must have a unique id. The id is used to identify the Crazyflie in the ROS2 namespace, e.g. ``/cf1`` for the Crazyflie with id 1. The id must be in the range between 0 and 255.

The channel of a crazyflie sets the radio frequency it uses to communicate. As described `here <https://www.bitcraze.io/documentation/repository/crazyradio2-firmware/main/functional-areas/usb-api/#channel>`_ a channel of 0 corresponds to the frequency 2400 MHz, a channel of 1 corresponds to 2401 MHz, and so on. The channel must be between 0 and 100. 

Each crazyradio can support one channel at a time. If e.g. you are using 10 Crazyflies on one radio they all need to be on the same channel.

.. note:: 
    When using multiple radios the channels should be spread apart to avoid interference. For e.g. two radios we are using channels 80 and 100, in another setup 50 and 100. By changing the channel(frequency) you can avoid interferences with WiFi and other 2.4Ghz communication.

Crazyflies per radio
--------------------

The modified crazyradio firmware is able to send and receive 1000 messages per second. Depending on your application you might need more or less messages per second per crazyflie which limits the amount of crazyflies on each channel/radio.

The crazyflie_node is setup to poll the battery and other vital information with a frequency of 1Hz. 
In our application we are using an external tracking system which provides the Crazyflies with positions at a frequency of 20Hz, these positions are sent with broadcasting packets however which manage to provide position data for 4 crazyflies per message. 

For 20 crazyflies (single radio) this results in a total of 20 (state) + (20 / 4) * 20 (position) = 120Hz of communication. 

When flying we send target positions at a frequency of 10Hz for each crazyflie.
If all crazyflies are in flight this results in a total of only 120Hz + 10Hz * 20  = 320Hz of communication.
If all works well therefore it is no issue to use these 20 crazyflies on a single radio.

In our setup approximately 5% off all messages are lost, which might be different depending on your environment.
In our application we have the 50 crazyflies split up into 2 radios, each with 25 crazyflies. 

.. note:: 
    Because the crazyflie prints lots of messages at bootup you dont want to have too many crazyflies on a single radio.
    Otherwise "loading in a new crazyflie" will become very slow.


