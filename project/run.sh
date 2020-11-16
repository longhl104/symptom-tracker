#!/bin/bash

export FLASK_ENV=development
export FLASK_APP=main

gunicorn --bind=0.0.0.0:8087 --log-level=debug main:app
