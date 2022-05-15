# Third party imports
import click

# Application Imports
from app_models import BlogRunner
from language_moderator import DUMMY_MODERATOR_ENDPOINT


@click.command()
@click.option("--host", default="0.0.0.0", type=str)
@click.option("--port", default=5000, type=int)
@click.option("--moderator_endpoint", default=DUMMY_MODERATOR_ENDPOINT, type=str)
def main(host, port, moderator_endpoint):
    blog_runner = BlogRunner(host, port, moderator_endpoint)
    blog_runner.run_service()


if __name__ == "__main__":
    main()
