#!/usr/bin/env python
import os
import subprocess
import click
from flask import Flask
from app import createApp

APP = createApp()

@click.group()
def cli():
    """Management script for the Flask application."""
    pass

@cli.command()
def run():
    """Runs the set-up needed for local development."""
    APP.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)

@cli.command()
def setup_prod():
    """Runs the set-up needed for production."""
    setup_general()

def setup_general():
    """Runs the set-up needed for both local development and production.
       Also sets up first admin user."""
    print("General setup for production and development.")

@cli.command()
def format():
    """Runs the yapf and isort formatters over the project."""
    isort = 'isort *.py app/'
    yapf = 'yapf -r -i *.py app/'

    print('Running {}'.format(isort))
    subprocess.call(isort, shell=True)

    print('Running {}'.format(yapf))
    subprocess.call(yapf, shell=True)

if __name__ == '__main__':
    cli()
