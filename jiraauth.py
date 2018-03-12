# NOTE: you must have jira-python in your PYTHONPATH for this to work
from jira.client import JIRA
from jira.jirashell import process_config

'''
This script assumes the existence of ~/.jira-python/jirashell.ini
with format like:

[options]
server = https://genymobile.atlassian.net

[basic_auth]
username = afouques
password = (optional)YourPassword

If you do not wish to use a config file, you can initialize a client
like this:

jclient = JIRA(options, basic_auth=('afouques', 'YourPassword'))

# This can also be made to work with oauth credentials
# See https://jira-python.readthedocs.org/en/latest/#authentication
'''

options, basic_auth, oauth = process_config()

jclient = None
password = None
if not basic_auth.has_key('username'):
    # Assume anonymity
    jclient = JIRA(options=options)
else:
    if basic_auth.has_key('password'):
        password = basic_auth['password']
    else:
        import getpass
        password = getpass.getpass(options['server'] + ' password: ') 
    jclient = JIRA(options=options,
                   basic_auth=(basic_auth['username'], 
                               password))

