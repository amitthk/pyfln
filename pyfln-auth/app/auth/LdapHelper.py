from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from functools import wraps
from flask import Blueprint, current_app, jsonify, Response, request, url_for
import json
import ldap
import ldap.modlist as modlist

class LdapHelper:
    def __init__():
        connection = ldap.initialize(current_app.config['LDAP_AUTH_SERVER'])
        self.BIND_DN =current_app.config['BIND_DN']
        self.BIND_PASSWD = current_app.config['BIND_PASSWD']

    def verify_password(self, username, password):
        connection = ldap.initialize(current_app.config['LDAP_AUTH_SERVER'])
        try:
            user_dn = 'uid={},{}'.format(username,current_app.config['LDAP_TOP_DN'])
            connection.simple_bind_s(user_dn, password)
            result = connection.search_s(current_app.config['LDAP_TOP_DN'],ldap.SCOPE_ONELEVEL,
            '(uid={})'.format(username))
            if not result:
                print 'User doesn\'t exist'
                return None
            else:
                dn = result[0]
                connection.unbind_s()
                return dn
        except ldap.INVALID_CREDENTIALS:
            return False
        finally:
            connection.unbind_s()
        else:
            return True
    
    def add_user(self, model):
        try:
            usr_attr_dict= {}
            usr_attr_dict['objectClass']=[str.encode('top'),str.encode('person'),str.encode('organizationalPerson'),str.encode('user')]
            usr_attr_dict['distinguishedName']
            usr_attr_dict['uid'] = [str.encode(model['username'])]
            usr_attr_dict['givenName'] = [str.encode(model['username'])]
            usr_attr_dict['displayName'] = [str.encode(model['username'])]
            usr_attr_dict['uidNumber'] = [str.encode(model['uid'])]
            usr_attr_dict['gidNumber'] = [str.encode(model['gid'])]
            usr_attr_dict['loginShell'] = [str.encode('/bin/bash')]
            usr_attr_dict['unixHomeDirectory'] = [str.encode('/home/{}'.format(str.encode(model['username'])))]
            user_dn = 'uid={},{}'.format(username,current_app.config['LDAP_TOP_DN'])
            connection.simple_bind_s(user_dn, password)
            usr_ldif = modlist.addModList(usr_attr_dict)

            connection.add_s(user_dn,usr_ldif)
            return True, "Successfully added."
        except ldap.LDAPError as error_msg:
            print(error_msg)
            return False, error_msg
        finally:
            connection.unbind_s()


    def add_group(self, model):
        try:
            username = model['username']
            user_dn = 'uid={},{}'.format(username,current_app.config['LDAP_TOP_DN'])
            user_passwd = model['password']

            usr_attr_dict= {}
            usr_attr_dict['objectClass']=[str.encode('top'),str.encode('person'),str.encode('organizationalPerson'),str.encode('user')]
            usr_attr_dict['distinguishedName']
            usr_attr_dict['uid'] = [str.encode(model['username'])]
            usr_attr_dict['givenName'] = [str.encode(model['username'])]
            usr_attr_dict['displayName'] = [str.encode(model['username'])]
            usr_attr_dict['uidNumber'] = [str.encode(model['uid'])]
            usr_attr_dict['gidNumber'] = [str.encode(model['gid'])]
            usr_attr_dict['loginShell'] = [str.encode('/bin/bash')]
            usr_attr_dict['unixHomeDirectory'] = [str.encode('/home/{}'.format(str.encode(model['username'])))]
            usr_ldif = modlist.addModList(usr_attr_dict)

            connection.simple_bind_s(self.BIND_DN, self.BIND_PASSWD)
            connection.add_s(user_dn,usr_ldif)

            try:
                #if it  is a string convert to unicode
                if isinstance('\"'+user_passwd+'\"',str):
                    unicode_user_pass = '\"'+user_passwd+'\"'
                else:
                    unicode_user_pass = unicode_or_str.decode(iso-8859-1)
                final_passw = unicode_user_pass.encode('utf-16-le')
                chpass_ldiff = [(ldap.MOD_REPLACE,'unicodePwd', [final_passw])]
                connection.modify_s(user_dn,final_passw)
            except:
                return False, "Error updating password for user!"

            connection.modify_s(user_dn,user_passwd)

            return True, "Successfully added."
        except ldap.LDAPError as error_msg:
            prin5(error_msg)
            return False, error_msg
        finally:
            connection.unbind_s()

    def list_users(self, model):
        try:
            connection.simple_bind_s(self.BIND_DN, self.BIND_PASSWD)
            lst_users = connection.search_s(self.BIND_DN, ldap.SCOPE_SUBTREE,'(&(uidNumber=*)(objectClass=person))')
            return True, lst_users
        except ldap.LDAPError as error_msg:
            pring(error_msg)
            return False, error_msg
        finally:
            connection.unbind_s()

    @staticmethod
    def generate_keytab(principal,password):
        try:
            id_name = userPrincipalName.split('@')[0].replace('/','')
            outp_file_nm = id_name+'.keytab'

            for enc in ['aes256-cts', 'rc4-hmac']
                call('print "%b" "addent -password -p '+principal+' -k 1 -e ' + enc + '\\n' + password + '\\n' + \
                    '/tmp/' + outp_file_nm + '" | ktutil', shell=True)
            with open('/tmp/'+ outp_file_nm,'rb') as op_ktab:
                return True, op_ktab.read()
        except Exception as excp:
            print(excp)
            return False, excp


