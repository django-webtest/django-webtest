#!/usr/bin/env python
import sys

from setuptools import setup


version = '1.9.13'


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
        "with Django's testing framework."
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
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.0',
        'Framework :: Django :: 5.1',
        'Framework :: Django :: 5.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
    ],
    project_urls={
        'Code': 'https://github.com/django-webtest/django-webtest',
        'Issue Tracker': 'https://github.com/django-webtest/django-webtest/issues',
        'Changelog': 'https://github.com/django-webtest/django-webtest/blob/master/CHANGES.rst',
    },
    keywords=['django', 'webtest', 'pytest'],
)
