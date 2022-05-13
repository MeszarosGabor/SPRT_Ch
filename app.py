# Standard library imports
from datetime import datetime

# Third party imports
from flask import Flask, request
from flask_restful import Api, Resource

# Application Imports
from language_moderator import moderate_entry


app = Flask(__name__)
api = Api(app)


DATABASE = {}


class BlogPostRegister(Resource):
    database = DATABASE

    def post(self):
        blog_entry = request.json
        tstmp = datetime.utcnow().timestamp()
        moderated_entry = moderate_entry(blog_entry)
        self.database[tstmp] = moderated_entry

    def get(self):
        return self.database


def main():
    api.add_resource(BlogPostRegister, "/posts/")
    app.run(host="0.0.0.0")


if __name__ == "__main__":
    main()
