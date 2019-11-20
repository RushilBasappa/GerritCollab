import click

@click.group()
def cli():
    pass

@cli.command()
@click.argument('cl')
def pull(cl):
    click.echo('CL: %s' % cl)
