import click
from deploy import deploy_function
from invoke import invoke_function


@click.group()
def cli():
    pass

@cli.command()
@click.argument("function_name")
def deploy(function_name):
    deploy_function(function_name)
    
@cli.command()
@click.argument("function_name")
@click.option("--data", default="{}", help="JSON payload")
def invoke(function_name, data):
    invoke_function(function_name, data)

if __name__ == "__main__":
    cli()
