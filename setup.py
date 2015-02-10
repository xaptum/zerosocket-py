#!/usr/bin/env python

from distutils.core import setup



setup(name='zclient',
      version='2.0',
      description='Xaptum Broker Client',
      author='Xaptum',
      author_email='social@xaptum.com',
      url='https://www.xaptum.com',
      package_dir = {'': 'src'},
      packages=['zclient'],
      data_files = [
          ('/etc/zclient/', ['src/html/index.html', 'src/html/logo.png', 'src/data/.cacert.pem', 'src/data/conf'])
      ]
     )
