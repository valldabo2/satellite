from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)


app.config['CORS_ALLOW_HEADERS'] = 'Content-Type'
app.config['CORS_METHODS'] = ["GET", "POST", "OPTIONS", "PUT", "DELETE"]
cors = CORS(app,
            resources={r"/*": {"origins": "*"}})

import project.routes
