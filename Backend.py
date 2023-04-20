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

# authorized user login
masterPassword = "strongpassword123"
masterUsername = 'username'

# Show all employees in database
@app.route('/', methods=['GET'])
def show_employees():
    sql = "SELECT * FROM Employee"
    cursor.execute(sql)
    results = cursor.fetchall()
    return jsonify(results)

app.run()