#!/usr/bin/env python
from setuptools import setup
from setuptools import find_packages

version = '0.0.2'

classifiers = ["Development Status :: 1 - Planning",
               "License :: OSI Approved :: Apache Software License",
               "Programming Language :: Python",
               "Programming Language :: Python :: 2.7",
               "Programming Language :: Python :: 3.2",
               "Programming Language :: Python :: 3.3",
               "Programming Language :: Python :: Implementation :: PyPy"]

setup(name='debris',
      version=version,
      description="Cache objects, web requests and page builds",
      long_description="""Methods to manange data effectively through 
                          asset controls.""",
      classifiers=classifiers,
      keywords="cache tornado memcache memory ram mongodb redis assets",
      author='@stevepeak',
      author_email='steve@stevepeak.net',
      url='http://github.com/stevepeak/debris',
      license='http://www.apache.org/licenses/LICENSE-2.0',
      packages=find_packages(exclude=["tests"]),
      include_package_data=True,
      zip_safe=True,
      install_requires=[],
      entry_points=None)
