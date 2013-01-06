from setuptools import setup
import os

def read(filename):
  with open(filename) as fin:
    return fin.read()

setup(
  name='jstree',
  version='0.1',
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
  description='',
  long_description=read('README.txt') if os.path.exists('README.txt') else '',
  requires=['dictobj'],
  py_modules=['jstree'],
  test_suite='jstree_test',
  )
