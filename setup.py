#!/usr/bin/env python3
from setuptools import setup, find_packages
import os

name="modbus_generator"
with open("README.md", 'r') as f:
    description = f.read()

datadir = os.path.join('share', 'name', 'templates')
datafiles = [(d, [os.path.join(d,f) for f in files]) for d, folders, files in os.walk(datadir)]

setup(name=name,
    version='1.0.1',
    description=description,
    url='https://github.com/snhobbs/ModbusRegisterMapping',
    author='ElectroOptical Innovations, LLC.',
    author_email='simon.hobbs@electrooptical.net',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'jinja2',
        'click'
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
    scripts=("bin/modbus_generator",),
    include_package_data=True,
    zip_safe=True,
    data_files=datafiles
)


