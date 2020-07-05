import config
from fx import quickQuery
from fx import quickWrite
import glob
import shutil
import os
import MySQLdb

# specify export details
cwd = os.getcwd()
exportPath = cwd + '/export/'
fnTables = exportPath + '/createTables.sql'
# if export directory does not exist, make it
if not os.path.exists(exportPath):
    os.mkdir(exportPath)

# get database parameters
sourceDB = config.sourceDB

# get list of tables
tables = glob.glob(config.sourcePath + '/' + sourceDB + '/*.ibd')

# get table names
tables = [table.split('/')[-1].split('.ibd')[0] for table in tables]

# get db connections
dbSource = MySQLdb.connect(
    host=config.sourceHost,
    user=config.sourceUser,
    passwd=config.sourcePassword,
    database=config.sourceDB)

# if table export exists, remove it
if os.path.exists(fnTables):
    os.remove(fnTables)
# remove foreign key constraint in table export script
quickWrite(fnTables, 'set foreign_key_checks = 0;')

# loop over tables
for table in tables:
    print(table)
    # get create table syntax and write to table export script
    query = 'SHOW CREATE TABLE `' + table + '`;'
    result = quickQuery(dbSource, query)
    quickWrite(fnTables, result[0][1] + ';')
    # export and move table backup to export directory
    query = 'FLUSH TABLE ' + table + ' FOR EXPORT;'
    result = quickQuery(dbSource, query)
    shutil.copy(config.sourcePath + '/' + sourceDB + '/' + table + '.ibd', exportPath)
    # unlock database
    query = 'UNLOCK TABLES;'
    result = quickQuery(dbSource, query)
# add foreign key constraint in table export script
quickWrite(fnTables, 'set foreign_key_checks = 1;')

# close database
dbSource.close()

