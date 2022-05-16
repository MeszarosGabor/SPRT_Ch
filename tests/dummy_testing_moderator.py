from flask import Flask, request
from flask_restful import Api, Resource


class TestModerator(Resource):
    """
    Test moderator that deems sentences foul if they
    contain the prescribed substring.
    """
    def __init__(self, trigger_string):
        self.trigger_string = trigger_string

    def get(self):
        return "I am up!"

    def post(self):
        sentence = request.json.get("fragment")
        print(f"Testing fragment: {sentence}")
        return {"has_foul_language": self.trigger_string in sentence.lower()}


class TestModeratorRunner:
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
