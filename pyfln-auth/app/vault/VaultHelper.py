from flask import current_app as app
import hvac

class VaultHelper:
    def __init__(self):
        self.VAULT_ADDR = app.config.get('VAULT_ADDR')
    
    def list_policy(self, ldap_id,ldap_pass, policy_name):
        try:
            if ldap_id is None:
                raise Exception('ldap user id cannot be null')
            if ldap_pass is None:
                raise Exception('ldap password cannot be null')
            if policy_name is None:
                raise Exception('policy name cannot be null')
            hvclient = hvac.Client(url=self.VAULT_ADDR,verify=False)
            auth = hvclient.ldap.login(ldap_id,ldap_pass)
            result = hvclient.get_policy(policy_name)
            hvclient.logout()
            return result
        except Exception, exc:
            raise

    def withdraw_secret(self, ldap_id="",ldap_pass="", secret_name=""):
        try:
            if ldap_id is None:
                raise Exception('ldap user id cannot be null')
            if ldap_pass is None:
                raise Exception('ldap password cannot be null')
            if secret_name is None:
                raise Exception('secret key cannot be null')
            print(self.VAULT_ADDR)
            hvclient = hvac.Client(url=self.VAULT_ADDR,verify=False)
            auth = hvclient.auth_ldap(ldap_id,ldap_pass)
            result = hvclient.read(secret_name)
            hvclient.logout()
            return result
        except Exception, exc:
            raise