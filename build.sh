#!/bin/bash

# Build the project
echo "Building the project..."
pip install -r requirements.txt
python3.9 manage.py collectstatic


echo "Collect Static..."
python3.9 manage.py collectstatic --noinput --clear