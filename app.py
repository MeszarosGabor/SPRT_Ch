# Standard library imports
from datetime import datetime

# Third party imports
import click
from flask import Flask, request
from flask_restful import Api, Resource

# Application Imports
from language_moderator import moderate_entry, DEFAULT_MODERATOR_ENDPOINT


class BlogPostRegister(Resource):
    
    def __init__(self, database, moderator_endpoint):
        self.database = database
        self.moderator_endpoint = moderator_endpoint

    def post(self):
        blog_entry = request.json
        tstmp = int(datetime.utcnow().timestamp())
        moderated_entry = moderate_entry(blog_entry)
        self.database[tstmp] = moderated_entry

    def get(self):
        return self.database


class BlogRunner:
    def __init__(self, host, port, moderator_endpoint):
        self.host = host
        self.port = port
        self.moderator_endpoint = moderator_endpoint
        self.database = {}

    def run_service(self):
        app = Flask(__name__)
        api = Api(app)
        api.add_resource(BlogPostRegister,
                         "/posts/",
                         resource_class_args=(self.database, self.moderator_endpoint))
        app.run(host=self.host, port=self.port)


@click.command()
@click.option("--host", default="0.0.0.0", type=str)
@click.option("--port", default=5000, type=int)
@click.option("--moderator_endpoint", default=DEFAULT_MODERATOR_ENDPOINT, type=str)
def main(host, port, moderator_endpoint):
    blog_runner = BlogRunner(host, port, moderator_endpoint)
    blog_runner.run_service()


if __name__ == "__main__":
    main()
