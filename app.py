# Standard library imports
from datetime import datetime

# Third party imports
from flask import Flask, request
from flask_restful import Api, Resource

# Application Imports
from language_moderator import moderate_entry


class BlogPostRegister(Resource):
    
    def __init__(self, DATABASE):
        self.database = DATABASE

    def post(self):
        blog_entry = request.json
        tstmp = datetime.utcnow().timestamp()
        moderated_entry = moderate_entry(blog_entry)
        self.database[tstmp] = moderated_entry

    def get(self):
        return self.database


class BlogRunner:
    def __init__(self):
        self.database = {}

    def run_service(self):
        app = Flask(__name__)
        api = Api(app)
        api.add_resource(BlogPostRegister,
                         "/posts/",
                         resource_class_args=(self.database,))
        app.run(host="0.0.0.0")


if __name__ == "__main__":
    blog_runner = BlogRunner()
    blog_runner.run_service()
