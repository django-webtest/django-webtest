#!/usr/bin/env python
from distutils.core import setup

version='1.0.2'

setup(
    name='django-webtest',
    version=version,
    author='Mikhail Korobov',
    author_email='kmike84@gmail.com',

    packages=['django_webtest'],

    url='http://bitbucket.org/kmike/django-webtest/',
    download_url = 'http://bitbucket.org/kmike/django-webtest/get/tip.zip',
    license = 'MIT license',
    description = """ Instant integration of Ian Bicking's WebTest
(http://pythonpaste.org/webtest/) with django's testing framework.""",

    long_description = open('README.rst').read(),
    requires = ['WebTest'],

    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ),
)