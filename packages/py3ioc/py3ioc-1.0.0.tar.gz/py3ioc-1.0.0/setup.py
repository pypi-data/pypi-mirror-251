# coding=utf-8

from setuptools import setup

setup(
    name='py3ioc',
    version='1.0.0',
    packages=['py3ioc'],
    include_package_data=True,
    url='https://github.com/atanistra/pyioc',
    license='MIT',
    author='Jakub (Mr. UPGrade) Czapliński / atanistra',
    author_email='pypi@serwis.atamail.eu',
    description='Python 3 IoC tools.',
    long_description='''
        Python 3 IoC tools.
        https://github.com/atanistra/pyioc/README.MD
        ''',
    install_requires=[
        'enum34>=1.1.1',
    ],
    extras_require={
        'test': [
            'pytest>=2.8.0',
            'mock>=1.3.0',
            'coverage>=4.0.0'
        ],
        'dev': [
            'ipython',
            'flake8'
        ],
        'doc': [
            'sphinx'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ]
)
