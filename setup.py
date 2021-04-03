#!/usr/bin/env python3
from setuptools import setup, find_packages
from glob import glob
with open("README.md", 'r') as f:
    description = f.read()

setup(name='modbus_generator',
    version='1.0.1',
    description=description,
    url='',
    author='ElectroOptical Innovations, LLC.',
    author_email='simon.hobbs@electrooptical.net',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'jinja2',
        'data-store',
        'click'
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    scripts=list(glob("bin/*")),
    include_package_data=True,
    zip_safe=True
)
