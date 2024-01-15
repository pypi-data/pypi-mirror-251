import click


@click.command()
@click.option('--mode', default='interactive', help='Interactive mode', type=click.Choice(['interactive', 'cli', 'json']))
def clone(mode: str):
    if mode == 'interactive':
        click.echo(f'{mode} mode coming soon!')
    elif mode == 'cli':
        click.echo(f'{mode} mode coming soon!')
    elif mode == 'json':
        click.echo(f'{mode} mode coming soon!')
    else:
        raise ValueError(f'Unknown mode: {mode}')
