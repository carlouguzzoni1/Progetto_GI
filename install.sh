#!/bin/bash

python3 -m build
cd dist
python3 -m pip install sampleproject-3.0.0-py3-none-any.whl
