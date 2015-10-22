import os
import logging

from flask import Flask, render_template, url_for, g, session, flash, redirect, request
# from flask.ext import restful
# from flask.ext.restful import reqparse, Api
# from flask.ext.sqlalchemy import SQLAlchemy
# from flask.ext.bcrypt import Bcrypt
# from flask.ext.httpauth import HTTPBasicAuth

basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../')

app = Flask(__name__)
app.config.from_object('app.config')
app.secret_key = '"*\x995\x9a\xf9\xf2\x13z\xd3\x9c=\x18u\xef\xf8\x90WD\xa3\xe5\xe1\x19\xb7'

logging.basicConfig(level=logging.DEBUG)

'''
Later these steps should be pulled from the database, possibly an admin
page to change these from a web interface

For now, set manually in the app config
'''
DEPLOY_STEPS = [
    {
        'name': 'Connect to Hanlon API',
        'detail': "Enter the URL for Hanlon API in order to retrieve discovered hosts.",
        'url': '/',
        'id': 'base'
    },
    {
        'name': "Select Hosts for Deployment",
        'detail': "Select which discovered hosts will be used in deployment.",
        'url': '/hosts',
        'id': 'hosts'
    },
    {
        'name': "Define Group Variables",
        'detail': "Define group-wide variables for deployment.",
        'url': '/group_vars',
        'id': 'group_vars'
    },
    {
        'name': "Define Host Variables",
        'detail': "Define per-host variables for deployments.",
        'url': '/host_vars',
        'id': 'host_vars'
    }
]

# # flask-sqlalchemy
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
# db = SQLAlchemy(app)
#
# # flask-restful
# api = restful.Api(app)
#
# # flask-bcrypt
# flask_bcrypt = Bcrypt(app)
#
# # flask-httpauth
# auth = HTTPBasicAuth()

# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
#     return response

### Begin decorators ###
@app.before_request
def load_session_from_cookie():
    if 'hanlonURL' in session:
        # make sure URL isn't simply an empty string
        if session['hanlonURL'] != '':
            g.hanlonDefined = True
            logging.debug("Hanlon URL is defined, rendering tasks...")
            logging.debug("URL: %s", session['hanlonURL'])
            g.hanlonURL = session['hanlonURL']
    else:
        # check to see if we're navigating to a step without the API defined
        if request.path != '/':
            flash("Hanlon API endpoint not defined.", "warning")
            logging.debug("Request path: %s", str(request.path))
        g.hanlonDefined = False
        logging.debug("Handlon URL is not defined!")

    g.deploy_steps = DEPLOY_STEPS

### Begin views ###
@app.route('/')
def home():
    if g.hanlonDefined:
        flash('Hanlon API Endpoint already defined', 'warning')
    else:
        pass
    return render_template('hanlonconnect.html')

@app.route('/hosts')
@app.route('/hosts/<debug>')
def hosts(debug=None):
    if debug == 'debug':
        test_hosts = [
            {
                'hostname': 'controller1',
                'ipmi_ip': '10.0.0.1',
                'mgmt_ip': '172.0.0.1',
                'disks': ['disk1', 'disk2', 'disk3']
            },
            {
                'hostname': 'controller2',
                'ipmi_ip': '10.0.0.2',
                'mgmt_ip': '172.0.0.2',
                'disks': ['disk1', 'disk2', 'disk3']
            },
            {
                'hostname': 'controller3',
                'ipmi_ip': '10.0.0.3',
                'mgmt_ip': '172.0.0.3',
                'disks': ['disk1', 'disk2', 'disk3']
            },
            {
                'hostname': 'compute1',
                'ipmi_ip': '10.0.0.4',
                'mgmt_ip': '172.0.0.4',
                'disks': ['disk1', 'disk2', 'disk3']
            },
            {
                'hostname': 'compute2',
                'ipmi_ip': '10.0.0.5',
                'mgmt_ip': '172.0.0.5',
                'disks': ['disk1', 'disk2', 'disk3']
            },
            {
                'hostname': 'compute3',
                'ipmi_ip': '10.0.0.6',
                'mgmt_ip': '172.0.0.6',
                'disks': ['disk1', 'disk2', 'disk3']
            },
        ]
        return render_template('hostselect.html', hosts = test_hosts)

    return render_template('hostselect.html')

@app.route('/group_vars')
def group_vars():
    return render_template('group_vars.html')

@app.route('/host_vars')
def host_vars():
    return render_template('host_vars.html')
