Developer Guide
***************

Development work should generally take place on a properly configured development server which has all system dependancies installed.

Pre-Setup
=========

This project makes use of ``pew`` for managing Python virtualenvs. If you are using ``bash``, it would be useful to have something similar to the following in your ``~/.bashrc`` file:

::

    ### >>> Override with your specific paths you want to use <<< ###
    WORKSPACE=$USER_DIR
    export PROJECT_HOME=$WORKSPACE/projects
    export WORKON_HOME=$HOME/.virtualenvs

The ``PROJECT_HOME`` variable is set to a projects folder in the workspace. You can change ``projects`` name to the name of folder in which your project resides. ``WORKON_HOME`` variable is
path for the virtual environment. The default path for the virtual environment will be ``/Users/<username>/.local/share/virtualenvs``. A symlink for the virtualenvs folder would be created in the user's directory.
If there is no symlink created, you can create one. The symlink would be:

::

    .virtualenvs -> /Users/<username>/.local/share/virtualenvs

Initial Setup of Python Environment
===================================

Python development should be taken place in a virtual environment. You can create a virtual environment for the project using invoke. The name
of the created virtual environment is going to be ``bingmaps``.

::

    $ invoke env

The above command helps in creating the virtual environment with all system dependancies.

.. note::

 - All the invoke tasks must be executed from the root folder of the project.
 - All the invoke tasks will run better in Linux/Mac. These might not be compatible with Windows as the commands are different.
 - The project is entirely system-independent except for invoke tasks.
 - When you run ``invoke env`` command multiple times, the virtual environment will be deleted and created again with all the system dependencies each time.


Working on a Virtual Environment
================================

In order to work in the virtual environment created, you have to run the following command:

::

    $ pew workon bingmaps

If you want to exit from the current virtual environment, you have to run the following command:

::

    bingmaps$ exit

Development Tasks
=================

There are several tasks specified in this project. You can get a list of all the available tasks through the following command:

::

    $ invoke [--list|-l]
    # OR
    $ inv [--list|-l]

For a detailed help on a command, run:

::

    $ inv --help <command>

env.new
-------

This command helps in creating a new virtual environment with the package's name ``bingmaps``:

::

    $ invoke env.new
    # OR
    $ inv env.new

env.install
-----------

This command helps in installing all the system dependencies inside the virtual environment created (``bingmaps``):

::

    $ invoke env.install
    # OR
    $ inv env.install

env.remove
----------

This command helps in removing/deleting the virtual environment (``bingmaps``):

::

    $ invoke env.remove
    # OR
    $ inv env.remove

env.clean
---------

This command helps in removing some of the project independent folders/files:

::

    $ invoke env.clean
    # OR
    $ inv env.clean

Some of the project independent folders/files are:

 - ``__pycache__``
 - ``.cache``
 - ``.tox``
 - ``.coverage``
 - ``.egg``
 - ``.egg*``
 - ``dist``
 - ``build``

.. note::

 - When you run ``inv env`` command, the above env tasks run in an order (``env.clean``, ``env.remove``, ``env.new``, ``env.install``)


tests.unit
----------

This command helps in running all the unit tests:

::

    $ invoke test.unit
    # OR
    $ inv test.unit

tests.style
-----------

This command helps in running style checker (pep8 validations):

::

    $ invoke test.style
    # OR
    $ inv test.style

tests.errors
------------

This command helps in running static error analysis (pylint validations):

::

    $ invoke test.errors
    # OR
    $ inv test.errors

.. note::

 - When you run ``inv tests`` command, the above tests tasks run in an order (``tests.errors``, ``tests.style``, ``tests.unit``)

docs.build
----------

This command helps in building the documentation:

::

    $ invoke docs.build
    # OR
    $ inv docs.build

docs.serve
----------

This command helps in running a simple server and you can view ``index.html`` can be viewed in a browser:

::

    $ invoke docs.serve
    # OR
    $ inv docs.serve

docs.publish
------------

This command helps in building and pushing the docs to repository's github pages:

::

    $ invoke docs.publish
    # OR
    $ inv docs.publish

.. note::

 - When you run ``inv docs`` command, the above docs tasks run in an order (``docs.build``, ``docs.serve``)