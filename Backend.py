import flask
from flask import jsonify
from flask import request, make_response
import creds
from sql import create_connection
from sql import execute_read_query
from sql import execute_query 
# pip instal flask_cors
from flask_cors import CORS

# Set up application
app = flask.Flask(__name__) 
app.config["DEBUG"] = True

# Enable CORS
CORS(app)

# db info
myCreds = creds.Creds()
conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName) 
cursor = conn.cursor(dictionary = True)