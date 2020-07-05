import os
import glob
import config
import MySQLdb
from fx import quickQuery
import shutil

# get tables to import
cwd = os.getcwd()
importPath = cwd + '/export/'
tables = glob.glob(importPath + '/*.ibd')
targetDB = config.targetDB

# get table names
tables = [table.split('/')[-1].split('.ibd')[0] for table in tables]

# get db connections
dbTarget = MySQLdb.connect(
    host=config.targetHost,
    user=config.targetUser,
    passwd=config.targetPassword,
    database=config.targetDB)

# drop existing databaase
cmdDrop = '\"DROP DATABASE IF EXISTS ' + config.targetDB + ';\"'
cmd = 'mysql -u ' + config.targetUser + ' -p' + config.targetPassword + ' -e ' + cmdDrop
r = os.system(cmd)

# create new target database
cmdCreate = '\"CREATE DATABASE ' + config.targetDB + ' CHARACTER SET utf8 COLLATE utf8_general_ci;\"'
cmd = 'mysql -u ' + config.targetUser + ' -p' + config.targetPassword + ' -e ' + cmdCreate
r = os.system(cmd)

# create tables
cmd = 'mysql -u ' + config.targetUser + ' -p' + config.targetPassword + ' ' + config.targetDB + ' < ' + importPath + '/createTables.sql'
r = os.system(cmd)

# loop over tables
result = quickQuery(dbTarget, 'set foreign_key_checks = 0;')
for table in tables:
    print(table)
    # discard table space
    query = 'ALTER TABLE ' + table + ' DISCARD TABLESPACE;'
    result = quickQuery(dbTarget, query)
    # move file
    shutil.copy(importPath + table + '.ibd', config.targetPath + '/' + targetDB + '/' + table + '.ibd')
    # import table space
    query = 'ALTER TABLE ' + table + ' IMPORT TABLESPACE;'
    result = quickQuery(dbTarget, query)
result = quickQuery(dbTarget, 'set foreign_key_checks = 1;')

# close database
dbTarget.close()


