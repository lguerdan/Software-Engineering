# Copyright (c) Microsoft. All rights reserved. Licensed under the MIT license.
# See LICENSE in the project root for license information.
"""Main program for Microsoft Graph API Connect demo."""
import json
import sys
import uuid

# un-comment these lines to suppress the HTTP status messages sent to the console
#import logging
#logging.getLogger('werkzeug').setLevel(logging.ERROR)

import requests
from flask import Flask, redirect, url_for, session, request, render_template, jsonify
from flask_oauthlib.client import OAuth

# read private credentials from text file
client_id, client_secret, *_ = open('_PRIVATE.txt').read().split('\n')
if (client_id.startswith('*') and client_id.endswith('*')) or \
    (client_secret.startswith('*') and client_secret.endswith('*')):
    print('MISSING CONFIGURATION: the _PRIVATE.txt file needs to be edited ' + \
        'to add client ID and secret.')
    sys.exit(1)

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

# since this sample runs locally without HTTPS, disable InsecureRequestWarning
requests.packages.urllib3.disable_warnings()

msgraphapi = oauth.remote_app( \
    'microsoft',
    consumer_key=client_id,
    consumer_secret=client_secret,
    request_token_params={'scope': 'User.Read Mail.Send'},
    base_url='https://graph.microsoft.com/v1.0/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://login.microsoftonline.com/common/oauth2/v2.0/token',
    authorize_url='https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
                             )

@app.route('/')
def index():
    """Handler for home page."""
    return render_template('connect.html')

@app.route('/login')
def login():
    """Handler for login route."""
    guid = uuid.uuid4() # guid used to only accept initiated logins
    session['state'] = guid
    return msgraphapi.authorize(callback=url_for('authorized', _external=True), state=guid)

@app.route('/logout')
def logout():
    """Handler for logout route."""
    session.pop('microsoft_token', None)
    session.pop('state', None)
    return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
    """Handler for login/authorized route."""
    response = msgraphapi.authorized_response()

    if response is None:
        return "Access Denied: Reason={0}\nError={1}".format( \
            request.args['error'], request.args['error_description'])

    # Check response for state
    if str(session['state']) != str(request.args['state']):
        raise Exception('State has been messed with, end authentication')
    session['state'] = '' # reset session state to prevent re-use

    # Okay to store this in a local variable, encrypt if it's going to client
    # machine or database. Treat as a password.
    session['microsoft_token'] = (response['access_token'], '')
    # Store the token in another session variable for easy access
    session['access_token'] = response['access_token']
    me_response = msgraphapi.get('me')
    me_data = json.loads(json.dumps(me_response.data))
    username = me_data['displayName']
    email_address = me_data['userPrincipalName']
    session['alias'] = username
    session['userEmailAddress'] = email_address
    return redirect('main')

@app.route('/main')
def main():
    """Handler for main route."""
    if session['alias']:
        username = session['alias']
        email_address = session['userEmailAddress']
        return render_template('main.html', name=username, emailAddress=email_address)
    else:
        return render_template('main.html')


@app.route('/call_people')
def call_people():

   send_people_url = 'https://graph.microsoft.com/v1.0/me/people/'

   # set request headers
   headers = { 'Authorization' : 'Bearer {0}'.format(session['access_token']),
               'Accept' : 'application/json'}

   request_id = str(uuid.uuid4())
   instrumentation = {'client-request-id' : request_id,
                       'return-client-request-id' : 'true'}

   headers.update(instrumentation)
   response = requests.get(url=send_people_url,
                             headers=headers)
   resp = response.json()
   connections = {}
   for connection in resp['value']:
      connections[connection['displayName']] = connection['scoredEmailAddresses'][0]['relevanceScore']
      # scores.append(connection['scoredEmailAddresses'][0]['relevanceScore'])

   # print(response.text)
   return jsonify(connections)

@msgraphapi.tokengetter
def get_token():
    return session.get('microsoft_token')
