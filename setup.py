import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class Tox(TestCommand):
    user_options = [
        ('tox-args=', 'a', "Arguments to pass to tox")
    ]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = '-c tox.ini'

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # Import here because outside the eggs aren't loaded.
        import tox
        import shlex

        errno = tox.cmdline(args=shlex.split(self.tox_args))
        sys.exit(errno)


def read(fname):
    with(open(os.path.join(os.path.dirname('__file__'), fname))) as fp:
        return fp.read()

pkg = {}
exec(read(os.path.join('docMaker',
                       '__pkg__.py')), pkg)

requirements = os.path.join('requirements',
                            'production.txt')
readme = read('README.rst')
changelog = read('CHANGELOG.rst')
install_requires = read(requirements).split()
entry_points = {
    'console_scripts': [
    ]
}

setup(
    name=pkg['__package_name__'],
    version=pkg['__version__'],
    url=pkg['__url__'],
    license=pkg['__license__'],
    author=pkg['__author__'],
    author_email=pkg['__email__'],
    description=pkg['__description__'],
    long_description=readme + '\n\n' + changelog,
    packages=find_packages(exclude=['tests', 'tasks']),
    install_requires=install_requires,
    tests_require=['tox'],
    entry_points=entry_points,
    cmdclass={'test': Tox},
    test_suite='tests',
    keywords='docMaker',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Filesystems',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
    ]
)
