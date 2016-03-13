import os
from invoke import run, task
from .utils import cd


BUILD_DIR = 'docs/_build'
HTML_DIR = os.path.join(BUILD_DIR, 'html')


@task
def build():
    """Build Documentation"""
    run('rm -rf {0}'.format(BUILD_DIR))
    run('cd docs && make doctest && make html')


@task
def serve(port=8000):
    print('Serving docs on 127.0.0.1 port {0} ...'.format(port))
    run('cd {0} && python3 -m http.server {1}'.format(HTML_DIR, port))


@task(pre=[build])
def publish(remote='git@github.com:bharadwajyarlagadda/bingmaps.git'):
    cmds = [
        'touch .nojekyll',
        'git init',
        'git add .',
        'git commit -m "Build docs"',
        'git remote add origin {0}'.format(remote),
        'git push --force origin master:gh-pages'
    ]

    with cd(HTML_DIR):
        run('&&'.join(cmds))


@task(name='all', pre=[build, serve], default=True)
def all_():
    pass
