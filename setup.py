from pathlib import Path
from setuptools import setup

with open('README.rst') as fd:
    DESCRIPTION = fd.read()

CLASSIFIERS = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: LGPL License',
    'Programming Language :: Python :: 3.6',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

packages = [str(mod.parent) for mod in Path('unha2').rglob('__init__.py')]

setup(
    name='unha2',
    version='1.0a.dev1',
    description='A library for rocket chat',
    long_description=DESCRIPTION,
    author='Mathieu Pasquet',
    author_email='pypi@mathieui.net',
    license='LGPL',
    platforms=['any'],
    packages=packages,
    install_requires=['aiohttp'],
    classifiers=CLASSIFIERS
)
