# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='flipdot',
    version='0.1.0',
    description='Driver and Simulator for Alfa-Zeta Flip-Dot',
    long_description=readme,
    author='D Creemer',
    author_email='dcreemer@zachary.com',
    url='https://github.com/dcreemer/flipdot',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
