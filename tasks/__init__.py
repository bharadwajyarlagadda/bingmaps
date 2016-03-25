from invoke import Collection

from . import (
    env,
    docs,
    test
)


sub_tasks = {
    'env': env,
    'docs': docs,
    'tests': test
}


namespace = Collection(**sub_tasks)
