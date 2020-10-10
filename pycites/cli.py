#!/usr/bin/env python3
import click

from .cites_download import zip_file, csv_file, get_data

CONTEXT_SETTINGS = {'help_option_names': ['-h', '--help']}
@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--force_update', is_flag=True, default=False)
@click.option('--cleanup', is_flag=True, default=False)
def cli(force_update, cleanup):
    get_data(zip_file, csv_file, force_update=force_update, cleanup=cleanup)

