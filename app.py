"""
This is the main runner of the Blog Backend Service.
Execute as a standalone script with specified CLI options.
"""

# Standard library imports
import logging

# Third party imports
import click

# Application Imports
from app_models import BlogRunner


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


@click.command()
@click.option("--host", default="0.0.0.0", type=str)
@click.option("--port", default=5000, type=int)
@click.option("--moderator_endpoint", type=str)
def main(host, port, moderator_endpoint):
    blog_runner = BlogRunner(host, port, moderator_endpoint)
    blog_runner.run_service()


if __name__ == "__main__":
    main()
