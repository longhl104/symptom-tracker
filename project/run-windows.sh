#!/bin/bash

set FLASK_ENV=development
set FLASK_APP=app

gunicorn --bind=0.0.0.0:8087 --log-level=debug main:app
