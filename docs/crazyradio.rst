.. _crazyradio:

.. toctree::

Crazyradio
##########

.. toctree:: 
   :maxdepth: 100

A `Crazyradio 2.0 <https://www.bitcraze.io/products/crazyradio-2-0/>`_ must be used in order to use the full potential of this library. 
You can then follow  the `Getting started with the Crazyradio 2.0 <https://www.bitcraze.io/documentation/tutorials/getting-started-with-crazyradio-2-0/>`_ guide.


.. warning::

    USB permissions need to be set up in order to use the Crazyradio.
    Follow `this guide <https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/installation/usb_permissions/>`_ to do so.


In order to achieve the bandwidth need for controlling multiple crazyflies, a radio with the `Inline Mode <https://www.bitcraze.io/2025/12/new-crazyradio-2-0-swarm-optimized-firmware-5-1/>`_ must be used.
The firmware is only compatible with the Crazyradio 2.0. 

Flashing the firmware
-----------------------------

The firmware can be found `here <https://github.com/DynamicSwarms/crazyflie_hardware/blob/master/crazyradio_firmware/crazyradio2-5.3.uf2>`_.
Or you can download the firmware directly from bitcraze `here <https://github.com/bitcraze/crazyradio2-firmware>`_ (tested with version 5.3).

Plug in your Crazyradio2.0 with the button pressed, this will put the Crazyradio into bootloader mode.
The Crazyradio will then show up as a mass storage device named `Crazyradio`.
You can then drag and drop the `crazyradio2.uf2` file onto the Crazyradio, which will automatically flash the modified firmware.



Compiling custom firmware
=================

If you want to modify and compile the firmware yourself, you can follow the instructions below.
Instructions on building and flashing can be found `here <https://github.com/bitcraze/crazyradio2-firmware/blob/main/docs/building-and-flashing/build.md>`_.
Be sure to have the `Bitcraze Toolbelt  <https://www.bitcraze.io/documentation/repository/toolbelt/master/>`_ installed, as it is required to build the firmware.

You are now ready to :doc:`configure your Crazyflies. </crazyflie>`