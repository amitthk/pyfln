from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from functools import wraps
from flask import Blueprint, current_app, jsonify, Response, request, url_for
import json
import ldap


class AppAuth:
    @staticmethod
    def generate_auth_token(app, data, expiration=500):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'payload': data}).decode('utf-8')

    @staticmethod
    def verify_auth_token(app, auth_token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            token = auth_token
            if auth_token.startswith('Bearer '):
                token=auth_token[7:]
            data=s.loads(auth_token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        return s.dumps({'payload': data})

    @staticmethod
    def verify_password(username, password):
        connection = ldap.initialize(current_app.config['LDAP_AUTH_SERVER'])
        result = connection.search_s(
            current_app.config['LDAP_TOP_DN'],
            ldap.SCOPE_ONELEVEL,
            '(uid={})'.format(username)
            )
        if not result:
            print 'User doesn\'t exist'
            return False
        dn = result[0][0]
        try:
            connection.bind_s(dn, password)
        except ldap.INVALID_CREDENTIALS:
            return False
        else:
            connection.unbind_s()
            return True
            
def must_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            flask_restplus.abort(401, 'Requires authentication!')
        if AppAuth.verify_auth_token(app,auth_header) is None:
            flask_restplus.abort(403, 'Authentication token is expired or invalid!')
        return f(*args, **kwargs)
    return decorated

# EOF
