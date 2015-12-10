# -*- coding: utf-8 -*-

if __name__ == '__main__':
    import subprocess
    p = subprocess.check_output('tox -l', shell=True)
    for env in p.split('\n'):
        if env.strip():
            print('  - TOXENV=%s' % env.strip())
    print('')
