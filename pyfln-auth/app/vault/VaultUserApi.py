import sys
import os
import json
import configparser
from functools import wraps

import flask_restplus

from flask import Blueprint, request, abort, Response, jsonify, url_for, session
from flask_restplus import Api, Resource, fields, reqparse

from .VaultHelper import VaultHelper
from auth.LdapHelper import must_auth

DEBUG = True

blueprint = Blueprint('vault',__name__,url_prefix='/api/vault')
api = Api(blueprint)
ns = api.namespace('vault',description='Simple Flask Ldap App')

cred_req_model = api.model('credreqmodel',{
    'userid': fields.String(),
    'pass': fields.String(),
    'keyname': fields.String()
})

@ns.route("/list_policy")
class ListPolicy(Resource):
    # method_decorators=[must_auth]
    @api.expect(cred_req_model)
    def post(self):
        try:
            vaul_helper = VaultHelper()
            return Response(str(vaul_helper.list_policy(api.payload['userid'], api.payload['pass'], api.payload['keyname'])),status=200)
        except Exception, exc:
            return Response("Error listing policy: " + str(exc), status=500)

@ns.route("/read_secret")
class ReadSecret(Resource):
    # method_decorators=[must_auth]
    @api.expect(cred_req_model)
    def post(self):
        try:
            vaul_helper = VaultHelper()
            data = vaul_helper.withdraw_secret(ldap_id=api.payload['userid'], ldap_pass= api.payload['pass'], secret_name= api.payload['keyname'])
            val = data['data']['env']
            return Response(val,status=200)
        except Exception, exc:
            raise
            return Response("Error reading secret: " + str(exc), status=500)