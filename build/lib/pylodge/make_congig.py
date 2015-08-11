__author__ = 'ashwin'
import os
from os.path import expanduser
import ConfigParser

home = expanduser('~')
os.chdir(home)
pylodgeconf = os.path.join(home,'.pylodge', 'pylodge.cfg')
if not os.path.isdir(home +'/.pylodge'):
    os.makedirs('.pylodge')
    print 'created directory'
    pylodgeroot= os.path.join(home,'.pylodge')
    pylodgeconf = os.path.join(pylodgeroot,'pylodge.cfg')
    open(pylodgeconf, 'w').close()
    print 'created conf file'

config = ConfigParser.RawConfigParser()

# Add Configurations to the configfile
config.add_section('Authentication Details')
config.set('Authentication Details', 'username', 'Your TestLodge User Name')
config.set('Authentication Details', 'password', 'Your TestLodge Password')
config.set('Authentication Details', 'project_name', 'Your TestLodge Project')
config.set('Authentication Details', 'api_url', 'Your TestLodge API URL')


# Writing our configuration file to 'pylodge.cfg'
with open(pylodgeconf, 'wb') as configfile:
    config.write(configfile)