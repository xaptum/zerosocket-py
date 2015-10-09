#!/usr/bin/env python
import os
from distutils.core import setup

def get_data_files():
    dirs = ['src/html/', 'src/data/']
    files = []
    for d in dirs:
        files.extend( [(d+f) for f in os.listdir(d) if os.path.isfile(d+f)] )
    return files

setup(name='zclient',
      version='2.0',
      description='Xaptum Broker Client',
      author='Xaptum',
      author_email='social@xaptum.com',
      url='https://www.xaptum.com',
      package_dir = {'': 'src'},
      packages=['zclient'],
      data_files = [
          ('/etc/zclient/', get_data_files())
      ]
     )
