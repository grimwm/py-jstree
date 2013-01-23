from setuptools import setup
import os

def read(filename):
  fin = None
  data = None
  try:
    fin = open(filename)
    data = fin.read()
  finally:
    if fin is not None:
      fin.close()
  return data

setup(
  name='jstree',
  version='0.3',
  author='William Grim',
  author_email='william@grimapps.com',
  url='https://github.com/grimwm/py-jstree',
  classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
    ],
  description='A package that helps generate JSON data for jQuery jsTree.',
  long_description=read('README.txt') if os.path.exists('README.txt') else '',
  install_requires=['dictobj'],
  py_modules=['jstree'],
  test_suite='jstree_test',
  )
