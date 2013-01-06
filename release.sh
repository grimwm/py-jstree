#!/bin/bash

# Run build
pandoc README.md -w rst -o README.txt
python setup.py sdist upload
markdown README.md > index.html
zip pypi.zip index.html

# Do cleanup
rm -f README.txt index.html
rm -rf dist
rm -rf jstree.egg-info
rm -rf __pycache__
rm -f *.pyc
