from invoke import run, task

from .utils import package_name


def test_targets():
    """Returns the test targets which contain the main package and tests folder
    """
    return [package_name(), 'tests']


@task
def unit():
    """Run all unit tests"""
    targets = test_targets()
    run('py.test --cov {0} {1}'.format(targets[0], ' '.join(targets)))


@task
def style():
    """Run style checker"""
    run('pep8 {0}'.format(' '.join(test_targets())))


@task
def errors():
    """Run static error analysis"""
    run('pylint -E {0}'.format(' '.join(test_targets())))


@task(name='all', pre=[errors, style, unit], default=True)
def _all():
    """Run all tests"""
    pass
