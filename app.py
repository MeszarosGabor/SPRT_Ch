from datetime import datetime

from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

DATABASE = {}

class BlogPostRegister(Resource):
    database = DATABASE

    def post(self):
        blog_entry = request.json
        tstmp = datetime.utcnow().timestamp()
        self.database[tstmp] = blog_entry

    def get(self):
        return self.database


def main():
    api.add_resource(BlogPostRegister, "/posts/")
    app.run(host="0.0.0.0")


if __name__ == "__main__":
    main()
