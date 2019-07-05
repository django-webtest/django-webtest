#!/usr/bin/env python
import sys

from setuptools import setup


version = '1.9.7'


def _read(name):
    if sys.version_info[0] < 3:
        with open(name) as f:
            return f.read()
    else:
        with open(name, encoding='utf8') as f:
            return f.read()


def get_long_description():
    return _read('README.rst') + "\n\n" + _read('CHANGES.rst')


setup(
    name='django-webtest',
    version=version,
    author='Mikhail Korobov',
    author_email='kmike84@gmail.com',

    packages=['django_webtest'],

    url='https://github.com/django-webtest/django-webtest',
    license='MIT license',
    description=(
        "Instant integration of Ian Bicking's WebTest "
        "(http://docs.pylonsproject.org/projects/webtest/) "
        "with django's testing framework."
    ),

    long_description=get_long_description(),
    install_requires=['webtest >= 1.3.3'],

    entry_points="""
    [pytest11]
    django_webtest = django_webtest.pytest_plugin
    """,

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
    ],
)
