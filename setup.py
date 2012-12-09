#!/usr/bin/env python
import os
from setuptools import setup, find_packages

setup(
    name='django-oscar-ticketing',
    version=":versiontools:ticketing:",
    url='https://github.com/tangentlabs/django-oscar-ticketing',
    author="Sebastian Vetter",
    author_email="sebastian.vetter@tangentsnowball.com.au",
    description="Ticketing and customer support for Oscar",
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    keywords="django, oscar, e-commerce",
    license='BSD',
    platforms=['linux'],
    packages=find_packages(exclude=["sandbox*", "tests*"]),
    include_package_data=True,
    install_requires=[
        'Django>=1.4.2',
        'versiontools>=1.1.9',
        #'django-oscar>=0.5',
        'django-model-utils>=1.1.0',
        'django-extra-views>=0.5.2',
        'django-tastypie>=0.9.11',
    ],
    # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
    dependency_links = [
        'https://github.com/tangentlabs/django-oscar/tarball/master#egg=django-oscar-0.5',
    ],
    classifiers=[
      'Environment :: Web Environment',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: BSD License',
      'Operating System :: Unix',
      'Programming Language :: Python'
    ]
)
