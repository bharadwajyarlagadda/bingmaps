Developer Guide
***************

Development work should generally take place on a properly configured development server which has all system dependancies installed.

Initial Setup of Python Environment
===================================

Python development should be taken place in a virtual environment. You can create a virtual environment for the project using invoke. The name
of the created virtual environment is going to be ``bingmaps``.

::

    $ invoke env

The above command helps in creating the virtual environment with all system dependancies.

.. note::

 - All the invoke tasks must be executed from the root folder of the project.
 - When you run ``invoke env`` command multiple times, the virtual environment will be deleted and created again with all the system dependencies each time.
