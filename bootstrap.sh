#!/bin/sh
rm -r ./lib ./include ./local ./bin
virtualenv --clear .
./bin/pip install -U pip
./bin/pip install -r https://raw.githubusercontent.com/plone/buildout.coredev/5.2/requirements.txt
./bin/buildout
