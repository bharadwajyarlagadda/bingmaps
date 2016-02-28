from invoke import task
from invoke import run
import os
from .utils import (
    package_name,
    python_bin,
    clean_files
)


requirements = os.path.join('requirements',
                            'development.txt')


def verun(cmd):
    """Runs a command inside the virtual environment without
    invoking it

    Args:
        cmd(str): Command to be run in the virtual env
    Returns:
         None
    """
    run('pew in {0} {1}'.format(package_name(), cmd))


@task
def new():
    """Creates a new virtual environment with the package name.
    """
    run('pew new --dont-activate --python={0} '
        '{1}'.format(python_bin, package_name()))
    verun('pip install --upgrade wheel')
    verun('pip install --upgrade pip')


@task
def remove():
    """Removes the virtual environment with the package name.
    """
    run('pew rm {0}'.format(package_name()))


@task
def clean():
    """Cleans the directory. Removes .tox and eggs from the project folder
    """
    clean_files()


@task
def install():
    """Installs all the dependencies in the virtual
     environment
    """
    verun('pip install -r {0}'.format(requirements))


@task(pre=[clean, remove, new, install], default=True)
def init():
    """Performs all the operations to create the virtual environment
    """
    print("Installed everything under {0} "
          "virtual environment".format(package_name()))