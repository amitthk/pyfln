from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from functools import wraps
from flask import Blueprint, current_app, jsonify, Response, request, url_for
import json
import ldap, sha, base64
import ldap.modlist
from .Util import Util
class LdapHelper:
    def __init__(self):
        self.connection = ldap.initialize(current_app.config['LDAP_AUTH_SERVER'])
        self.BIND_DN =current_app.config['BIND_DN']
        self.ADMIN_DN =current_app.config['ADMIN_DN']
        self.BIND_PASSWD = current_app.config['BIND_PASSWD']
        self.ADMIN_PASSWD =current_app.config['ADMIN_PASSWD']
        self.BASE_DN = current_app.config['LDAP_TOP_DN']

    def verify_password(self, username, password):
        try:
            user_dn = 'uid={},{}'.format(username,self.BASE_DN)
            self.connection.simple_bind_s(user_dn, password)
            result = self.connection.search_s(self.BASE_DN,ldap.SCOPE_ONELEVEL,
            '(uid={})'.format(username))
            if not result:
                print 'User doesn\'t exist'
                return None
            else:
                dn = result[0]
                return dn
        except ldap.INVALID_CREDENTIALS:
            return False
        finally:
            self.connection.unbind_s()
    
    # def add_group(self, model):
    #     try:
    #         usr_attr_dict= {}
    #         usr_attr_dict['objectClass']=[str('top'),str('person'),str('organizationalPerson'),str('user')]
    #         usr_attr_dict['distinguishedName']
    #         usr_attr_dict['uid'] = [str(model['username'])]
    #         usr_attr_dict['givenName'] = [str(model['username'])]
    #         usr_attr_dict['displayName'] = [str(model['username'])]
    #         usr_attr_dict['uidNumber'] = [str(model['uid'])]
    #         usr_attr_dict['gidNumber'] = [str(model['gid'])]
    #         usr_attr_dict['loginShell'] = [str('/bin/bash')]
    #         usr_attr_dict['unixHomeDirectory'] = [str('/home/{}'.format(str(model['username'])))]
    #         user_dn = 'uid={},{}'.format(username,self.BASE_DN)
    #         self.connection.simple_bind_s(user_dn, password)
    #         usr_ldif = modlist.addModList(usr_attr_dict)

    #         self.connection.add_s(user_dn,usr_ldif)
    #         return True, "Successfully added."
    #     except ldap.LDAPError as error_msg:
    #         print(error_msg)
    #         return False, error_msg
    #     finally:
    #         self.connection.unbind_s()


    def add_user(self, model):
        try:
            self.connection = ldap.initialize(current_app.config['LDAP_AUTH_SERVER'])
            username = model['username']
            user_dn = 'uid={},{}'.format(username,self.BASE_DN)
            user_passwd = model['password']

            print('Here is the model being passed for creation: {0}'.format(str(model)))
            ctx = sha.new(str(model['password'])) 
            hash = "{SHA}" + base64.b64encode(ctx.digest())

            usr_ldif = Util.get_ldif(model,self.BASE_DN,self.ADMIN_DN,self.ADMIN_PASSWD)

            self.connection.add_s(user_dn,usr_ldif)

            # try:
            #     #if it  is a string convert to unicode
            #     if isinstance('\"'+user_passwd+'\"',str):
            #         unicode_user_pass = '\"'+user_passwd+'\"'
            #     else:
            #         unicode_user_pass = unicode_or_str.decode(iso-8859-1)
            #     final_passw = unicode_user_pass.encode('utf-16-le')
            #     chpass_ldiff = [(ldap.MOD_REPLACE,'unicodePwd', [final_passw])]
            #     self.connection.modify_s(user_dn,final_passw)
            # except:
            #     return False, "Error updating password for user!"

            # self.connection.modify_s(user_dn,user_passwd)

            return True, "Successfully added."
        except ldap.LDAPError as error_msg:
            print(error_msg)
            return False, error_msg
        finally:
            self.connection.unbind_s()

    def list_users(self, model):
        self.connection = ldap.initialize(current_app.config['LDAP_AUTH_SERVER'])
        try:
            self.connection.simple_bind_s(self.BIND_DN, self.BIND_PASSWD)
            lst_users = self.connection.search_s(self.BASE_DN, ldap.SCOPE_SUBTREE,'(&(uidNumber=*)(objectClass=person))')
            return True, lst_users
        except ldap.LDAPError as error_msg:
            pring(error_msg)
            return False, error_msg
        finally:
            self.connection.unbind_s()

    def generate_keytab(self, principal,password):
        try:
            id_name = userPrincipalName.split('@')[0].replace('/','')
            outp_file_nm = id_name+'.keytab'

            for enc in ['aes256-cts', 'rc4-hmac']:
                call('print "%b" "addent -password -p '+principal+' -k 1 -e ' + enc + '\\n' + password + '\\n' + \
                    '/tmp/' + outp_file_nm + '" | ktutil', shell=True)
            with open('/tmp/'+ outp_file_nm,'rb') as op_ktab:
                return True, op_ktab.read()
        except Exception as excp:
            print(excp)
            return False, excp

    def generate_token(self, data, expiration=500):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'payload': data}).decode('utf-8')
    
    def verify_auth_token(self, auth_token):
        s = Serializer(current_app.config['SECRET_KEY'])
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


def must_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            flask_restplus.abort(401, 'Requires authentication!')
        ldaphelper = LdapHelper()
        if ldaphelper.verify_auth_token(auth_header) is None:
            flask_restplus.abort(403, 'Authentication token is expired or invalid!')
        return f(*args, **kwargs)
    return decorated

