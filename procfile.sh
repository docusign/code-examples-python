#!/bin/sh

if [ "$DEBUG" = "True" ]; then
        FLASK_ENV="development"
        python run.py
else
        gunicorn app:app
fi
