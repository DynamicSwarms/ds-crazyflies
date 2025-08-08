.. _crazyradio:

.. toctree::

Crazyradio
##########

.. toctree:: 
   :maxdepth: 100

A `Crazyradio 2.0 <https://www.bitcraze.io/products/crazyradio-2-0/>`_ must be used in order to use the full potential of this library. 

.. warning::

    USB permissions need to be set up in order to use the Crazyradio.
    Follow `this guide <https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/installation/usb_permissions/>`_ to do so.


Because the performance of the original crazyradio firmware fails to accomplish a high data rate when multiple Crazyflies are connected, we provide a modified firmware.
The firmware is only compatible with the Crazyradio 2.0. 

The modified firmware can be found at `here <https://github.com/DynamicSwarms/crazyradio2-firmware>`_.
Instructions on building and flashing can be found `here <https://github.com/bitcraze/crazyradio2-firmware/blob/main/docs/building-and-flashing/build.md>`_.

Be sure to have the `Bitcraze Toolbelt  <https://www.bitcraze.io/documentation/repository/toolbelt/master/>`_ installed, as it is required to build the firmware.


.. note::

    The modified firmware is not compatible with any other crazyflie library, such as `Crazyswarm 2 <https://imrclab.github.io/crazyswarm2/>`_, `Crazyswarm <https://crazyswarm.readthedocs.io/en/latest/>`_ or the crazyflie-lib-python used by the `crazyflie client <https://www.bitcraze.io/documentation/repository/crazyflie-clients-python/master/>`_.


Modifications
-------------

The modifications are described in this `issue <https://github.com/bitcraze/crazyradio2-firmware/issues/9>`_.
The main improvements was to not change id and channel with `sendVendorSetup()` but insted use the `bulkTransfer()` usb communication to set the id and channel, as this does not waste time on the usb communication.

This improves the communication rate from ~300Hz to ~1000Hz when multiple Crazyflies are connected.


Legacy Compilation
...................

.. note::
    Currently the legacy compilation is not implemented. However, it is planned to be implemented in the future.

If the library is compiled in `legacy radio` mode it is possible to use either crazyradio 2.0 or Crazyradio PA.
You can then follow  the `Getting started with the Crazyradio 2.0 <https://www.bitcraze.io/documentation/tutorials/getting-started-with-crazyradio-2-0/>`_ guide.
Upload the latest CRPA emulation firmware (tested with `V1.2 <https://github.com/bitcraze/crazyradio2-firmware/releases/tag/1.2>`_)

If you are using a `Crazyradio PA <https://www.bitcraze.io/products/crazyradio-pa/>`_ specific firmware, only the `Crazyswarm <https://github.com/USC-ACTLab/crazyswarm>`_ or 
`Crazyswarm 2 <https://github.com/IMRCLab/crazyswarm2>`_ prebuilt folder needs to be used. This special firmware has the necessary broadcasting features implemented.
