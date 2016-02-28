from invoke import Collection

from . import (
    env,
    test
)


sub_tasks = {
    'env': env,
    'tests': test
}


namespace = Collection(**sub_tasks)
