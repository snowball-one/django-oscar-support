#!/usr/bin/env python
import os

from setuptools import setup, find_packages

from oscar_support import get_version


def location(path):
    return os.path.join(os.path.dirname(__file__))


setup(
    name='django-oscar-support',
    version=get_version(),
    url='https://github.com/tangentlabs/django-oscar-support',
    author="Sebastian Vetter",
    author_email="sebastian.vetter@tangentsnowball.com.au",
    description="Ticketing and customer support for Oscar",
    long_description=open(location('README.rst')).read(),
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
        'django-extra-views>=0.5.2',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Programming Language :: Python'
    ]
)
