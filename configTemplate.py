# packages
import os


# current working directory for convenience
cwd = os.getcwd()

# source properties
source_dbname = 'sourceDbName'
source_password = 'sourcePassword'
source_user = 'sourceUser'
source_host = 'localhost'
source_datapath = '/usr/local/var/mysql/'
source_export = cwd + '/export/'

# target properties
target_dbname = 'targetDbName'
target_password = 'targetPassword'
target_user = 'targetUser'
target_host = 'localhost'
target_datapath = '/usr/local/var/mysql/'
target_import = cwd + '/export/'
