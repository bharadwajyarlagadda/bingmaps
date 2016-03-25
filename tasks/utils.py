import os
from functools import partial
from invoke import run
from contextlib import contextmanager
from pathlib import Path


python_bin = 'python3'


@contextmanager
def cd(path):
    """Context manager that changes the current working directory to 'path'
    within the context and changes it back on exit"""
    original_path = os.getcwd()
    os.chdir(path)

    yield

    os.chdir(original_path)


def bash(cmd):
    """Execute command using /bin/bash instead of /bin/sh."""
    return run('/bin/bash -c "{0}"'.format(cmd))


def mkdir(*paths):
    """Create directories and any parent directory that doesn't exist"""
    for path in paths:
        run('mkdir -p {0}'.format(path))


def ls(path):
    """Return directory listing as generator"""
    return [str(item.parts[-1] for item in iterdir(path))]


def iterdir(path):
    """Return directory listing as generator"""
    return Path(path).iterdir()


def files(path):
    return (item for item in iterdir(path) if item.is_file())


def folders(path):
    return (item for item in iterdir(path) if item.is_dir())


def clean_files():
    """Remove temporary files related to development"""
    run('find . -name \*.py[cod] -type f -delete')
    run('find . -depth -name __pycache__ -type d -exec rm -rf {} \;')
    run('rm -rf .cache .tox .coverage .egg* *.egg* dist build')


def readout(cmd):
    """A command for getting the package name from
    setup.py file
    Args:
        cmd (str): 'python setup.py --name'
    Returns:
        str: package name
    """
    return run(cmd, hide='out').stdout.strip()


def get_package_property(name):
    """A command for getting the package name from
    setup.py file
    Args:
        name (str): '--name'
    Returns:
        str: package name
    """
    return readout('python setup.py '
                  '--{0}'.format(name))

package_name = partial(get_package_property, 'name')
package_version = partial(get_package_property, 'version')
