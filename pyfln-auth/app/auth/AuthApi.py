import sys
import os
import json
import configparser
from functools import wraps

import flask_restplus

from flask import Blueprint, request, abort, Response, jsonify, url_for, session
from flask import current_app as app
from flask_restplus import Api, Resource, fields, reqparse

from .LdapHelper import LdapHelper
from .LdapHelper import must_auth

DEBUG = True

blueprint = Blueprint('auth',__name__,url_prefix='/api/auth')
api = Api(blueprint)
ns = api.namespace('user',description='Simple Flask Ldap App')

login_model = api.model("loginmodel", {
    "username": fields.String("Username."),
    "password": fields.String("Password.")
})

add_user_model = api.model("add_user_model", {
    "username": fields.String("Username"),
    "password": fields.String("Password"),
    "uid": fields.String("uid"),
    "gid": fields.String("gid")
})


@ns.route("/auth_token")
class AuthToken(Resource):
    @api.expect(login_model)
    def post(self):
        error=None
        login_m = api.payload
        user = str(login_m['username'])
        passwd = str(login_m['password'])
        ldaphelper = LdapHelper()
        if ldaphelper.verify_password(user,passwd):
            session['logged_in'] = True
            return {'Basic': str(ldaphelper.generate_token(user))}
        else:
            error = 'Invalid Credentials, please try again later!'
            return auth_response()

@ns.route("/index")
class Home(Resource):
    method_decorators=[must_auth]
    def get(self):
        return json.dumps({'payload': ['You','Got','Data']})

@ns.route("/add_user")
class AddUser(Resource):
    #method_decorators=[must_auth]
    @api.expect(add_user_model)
    def post(self):
        ldaphelper  = LdapHelper()
        result,status = ldaphelper.add_user(api.payload)
        if result == True:
            return json.dumps({'payload': ['User','Was','Added']})
        else:
            return json.dumps({'error': str(status)})

def auth_response():
    message = {
        'error': 'unauthorized',
        'message': 'Please authenticate with a valid token',
        'status': 401
        }
    response = Response(
        json.dumps(message),
        401,
        {
            'WWW-Authenticate': 'Basic realm="Authentication Required"',
            'Location': url_for('pyfln_auth_token')
            }
        )
    return response

if __name__=="__main__":
    app.run(host='0.0.0.0')