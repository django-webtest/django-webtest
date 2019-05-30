# -*- coding: utf-8 -*-

TRAVIS_CONF = '''
language: python

cache:
  directories:
    - $HOME/.cache/pip

services:
  - postgresql
before_script:
  - psql -c 'create database django_webtest_tests;' -U postgres

install:
  - pip install tox
script:
  - tox
matrix:
  include:
'''

if __name__ == '__main__':
    import subprocess
    import sys
    p = subprocess.check_output('tox -l', shell=True)
    if sys.version_info.major == 3:
        p = p.decode('utf-8')
    with open('.travis.yml', 'w') as fd:
        fd.write(TRAVIS_CONF)
        for env in p.split('\n'):
            env = env.strip()
            if env and env not in ('travis',):
                dist = None
                if env.startswith('pypy'):
                    py = 'pypy'
                else:
                    py = '{0}.{1}'.format(env[2], env[3])
                    if int(env[2] + env[3]) > 36:
                        # looks like psql dos not work on xenial... skip 3.7
                        # for now
                        continue
                        dist = 'xenial'
                fd.write('    - python: "{}"\n'.format(py))
                fd.write('      env: TOXENV={}\n'.format(env))
                if dist is not None:
                    fd.write('      dist: {}\n'.format(dist))
