"""
Flask Restful application Resource models for the Blog service.
"""

# Standard library imports
import logging
from datetime import datetime

# Third party imports
from flask import Flask, request
from flask_restful import Api, Resource
from gevent.pywsgi import WSGIServer

# Application imports
from language_moderator import moderate_entry


logger = logging.getLogger()


class BlogPostRegister(Resource):
    """ Main entry of posting and retrieving posts. """

    def __init__(self, database, moderator_endpoint):
        self.database = database
        self.moderator_endpoint = moderator_endpoint

    def post(self):
        """
        Enters a new blog entry into the db.
        JSON payload format:
        {
            'title': <str>,
            'paragraphs': <List[str]>,
        }

        Upon insertion into the db we enhance the above JSON with a
        'has_foul_language' additional string field.
        """
        try:
            blog_entry = request.json
            tstmp = int(datetime.utcnow().timestamp())
            moderated_entry = moderate_entry(blog_entry,
                                             self.moderator_endpoint)
            self.database[tstmp] = moderated_entry
        # TODO: process exceptions with finer granularity
        except Exception as exc:
            return {"status": "Failed", "exc": str(exc)}
        else:
            return {"status": "Success"}

    def get(self):
        """ Returns the db content as a JSON object """
        # TODO: support per-title retrieval
        return self.database


class BlogRunner:
    """ The main runner class of the blog service. """

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
                         resource_class_args=(self.database,
                                              self.moderator_endpoint))
        http_server = WSGIServer((self.host, self.port), app)
        logger.info(f"Starting the main app at {self.host}:{self.port}...")
        http_server.serve_forever()
