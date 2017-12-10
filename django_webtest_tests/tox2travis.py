# -*- coding: utf-8 -*-

TRAVIS_CONF = '''
language: python
sudo: false

addons:
  postgresql: "9.3"
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
                if env.startswith('pypy'):
                    py = 'pypy'
                else:
                    py = '{0}.{1}'.format(env[2], env[3])
                fd.write('    - python: "{}"\n'.format(py))
                fd.write('      env: TOXENV={}\n'.format(env))
