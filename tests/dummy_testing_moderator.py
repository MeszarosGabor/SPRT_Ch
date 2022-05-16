"""
A simple moderator service for testing purposes.
"""

# Standard library imports
import logging

# Third party imports
from flask import Flask, request
from flask_restful import Api, Resource


logger = logging.getLogger()


class TestModerator(Resource):
    """
    Test moderator that deems sentences foul if they
    contain the prescribed substring.
    """
    def __init__(self, trigger_string):
        self.trigger_string = trigger_string

    def get(self):
        """
        Mostly for verification of the service,
        this get endpoint provides a 'heartbeat'.
        """
        return f"I am up! My trigger string is {self.trigger_string}"

    def post(self):
        """
        Returns if the given sentence contains the
        pre-described trigger word.
        """
        sentence = request.json.get("fragment")
        logging.debug(f"Testing fragment: {sentence}")
        return {"has_foul_language": self.trigger_string in sentence.lower()}


class TestModeratorRunner:
    """ Main runner of the moderator service. """
    def __init__(self, host, port, trigger_string):
        self.host = host
        self.port = port
        self.trigger_string = trigger_string

    def run_service(self):
        app = Flask(__name__)
        api = Api(app)
        api.add_resource(TestModerator,
                         "/",
                         resource_class_args=(self.trigger_string,))
        app.run(host=self.host, port=self.port, debug=True)
