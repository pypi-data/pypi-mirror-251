import click

from .clone import clone


@click.group()
def cli():
    pass


def main():
    cli.add_command(clone)
    cli()
