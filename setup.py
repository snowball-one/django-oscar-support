#!/usr/bin/env python
from setuptools import setup, find_packages


setup(
    name='django-oscar-support',
    version='0.1.0',
    url='https://github.com/tangentlabs/django-oscar-support',
    author="Sebastian Vetter",
    author_email="sebastian.vetter@tangentsnowball.com.au",
    description="Ticketing and customer support for Oscar",
    long_description=open('README.rst').read(),
    keywords="django, oscar, e-commerce, customer support, issue tracking",
    license='BSD',
    platforms=['linux'],
    packages=find_packages(exclude=["sandbox*", "tests*"]),
    include_package_data=True,
    install_requires=[
        'django-shortuuidfield',
        'Django>=1.4',
        'django-oscar',
        'django-extensions',
        'djangorestframework',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Programming Language :: Python'
    ]
)
