import ldap
import ldap.modlist
from flask import current_app

class Util:
    @staticmethod
    def get_ldif(model,BASE_DN,ADM_UID, ADM_PWD):
        username = model['username']
        user_dn = 'uid={},{}'.format(username,BASE_DN)
        usr_attr_dict= {}
        usr_attr_dict['objectClass']= [str('top'),str('person') ,str('organizationalPerson'),str('user'),str('posixAccount')]
        usr_attr_dict['distinguishedName']=[str(user_dn)]
        usr_attr_dict['uid'] = [model['username'].encode('ascii')]
        usr_attr_dict['givenName'] = [str(model['username'])]
        usr_attr_dict['displayName'] = [str(model['username'])]
        usr_attr_dict['uidNumber'] = [str(model['uid'])]
        usr_attr_dict['gidNumber'] = [str(model['gid'])]
        usr_attr_dict['loginShell'] = [str('/bin/bash')]
        usr_attr_dict['userPassword'] = [str(hash)]
        usr_attr_dict['homeDirectory'] = [str('/home/{}'.format(str(model['username'])))]
        #print(str(usr_attr_dict))
        l = ldap.initialize(current_app.config['LDAP_AUTH_SERVER'])
        #l.simple_bind_s(ADM_UID, ADM_PWD)
        usr_ldif = ldap.modlist.addModList(usr_attr_dict)
        return usr_ldif