import click
from .app.app import app

@click.command()
@click.option("--port", "-p", default=5000, type=int, required=False, help="Port to run the server on")
def cli(port:int):
  app.run(port=port)

if __name__ == "__main__":
	cli()