import flask
from flask import request, jsonify,Flask, render_template, redirect, url_for
import pandas as pd

app = flask.Flask(__name__)
app.config["DEBUG"] = True

df_all_users_more=pd.read_table(r'C:\PAN\python project\api\users.txt',delimiter="|",header=None, names=["ID","NAME","AGE","DOB","FirstName","LastName","Address_line1",
"Address_line_2","Address_line_3","Phone"],dtype = str)

df_all_users=df_all_users_more.filter(["ID","NAME","AGE","DOB","FirstName","LastName"], axis=1)


@app.route('/', methods=['GET'])
def home():
    return '''<h1>API for user list</h1>
<p>A prototype API for returning list of users.</p>'''


# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('html_table'))
    return render_template('login.html', error=error)

@app.route('/specific', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for user in user_list:
        if user['id'] == id:
            results.append(user)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

@app.route('/tab', methods=("POST", "GET"))
def html_table():
    return render_template('user_list_page.html',  tables=[df_all_users.to_html(classes='data')], titles=df_all_users.columns.values)
app.run()