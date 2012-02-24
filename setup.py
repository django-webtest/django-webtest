#!/usr/bin/env python
from distutils.core import setup

for cmd in ('egg_info', 'develop'):
    import sys
    if cmd in sys.argv:
        from setuptools import setup

version='1.5'

setup(
    name='django-webtest',
    version=version,
    author='Mikhail Korobov',
    author_email='kmike84@gmail.com',

    packages=['django_webtest'],

    url='https://bitbucket.org/kmike/django-webtest/',
    download_url = 'https://bitbucket.org/kmike/django-webtest/get/tip.zip',
    license = 'MIT license',
    description = """ Instant integration of Ian Bicking's WebTest
(http://pythonpaste.org/webtest/) with django's testing framework.""",

    long_description = open('README.rst').read() + open('CHANGES.txt').read(),
    requires = ['webtest'],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
    ],
)
