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
env:
'''

if __name__ == '__main__':
    import subprocess
    p = subprocess.check_output('tox -l', shell=True)
    with open('.travis.yml', 'w') as fd:
        fd.write(TRAVIS_CONF)
        for env in p.split('\n'):
            env = env.strip()
            if env and env not in ('travis',):
                fd.write('  - TOXENV={}\n'.format(env))
