#!/bin/sh
rm -r ./lib ./include ./local ./bin
virtualenv --clear .
./bin/pip install -U pip
./bin/pip install -r requirements.txt
./bin/buildout
