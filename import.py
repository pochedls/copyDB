#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Stephen Po-Chedley 5 July 2020

This is the export script as part of copyDB. It is intended to import
a MySQL database (that has been exported with export.py). It will:
    1) create all of the source database tables
    2) copy the source database tables into place

Parameters can be specified via the config.py file or via the command line.
The arguments needed (in config.py) are:
    * target_dbname       : target database to be created
    * target_password     : user of target database
    * target_user         : user password for target database
    * target_host         : host for target database
    * target_datapath     : path to underlining database files
    * target_import       : location of data to import

Alternatively, these can be specifed via command line arguments (see help):
    ./import.py --help

The environment was created / implemented using:
    conda create -n copydb mysql-connector-python mysqlclient ipython python=3
    conda activate copydb

Alternatively, these packages can be installed with pip:
    pip install mysqlclient
    pip install mysql-connector-python

@author: pochedls
"""

# package / function imports
import os
import sys
import glob
import config
import MySQLdb
from fx import quickQuery
from fx import str2bool
import shutil
import argparse


# check if interactive or not
try:
    __IPYTHON__
except NameError:
    INIPYTHON = False
else:
    INIPYTHON = True

# Look for cmd line arguments if we are NOT in Ipython
if INIPYTHON is False:

    parser = argparse.ArgumentParser()

    # Optional arguments
    parser.add_argument('-v', '--verbose', type=str2bool,
                        default=True,
                        help="Flag (TRUE/FALSE) to print out more " +
                             "information (default is TRUE)")

    parser.add_argument('-db', '--dbname', type=str,
                        help="Target database name")

    parser.add_argument('-u', '--user', type=str,
                        help="MySQL username for target database")

    parser.add_argument('-p', '--password', type=str,
                        help="MySQL user password for target database")

    parser.add_argument('-c', '--host', type=str,
                        help="MySQL host (e.g., localhost) for target " +
                        "database")

    parser.add_argument('-dp', '--datapath', type=str,
                        help="Path to MySQL database files " +
                        "(e.g., /usr/local/var/mysql/)")

    parser.add_argument('-e', '--importpath', type=str,
                        help="Path to import source database (e.g., import/)")

    # override any config options with command line options
    args = parser.parse_args()

    verbose = args.verbose
    for arg in vars(args):
        if getattr(args, arg) is None:
            locals()[arg] = getattr(config, 'target_' + arg)
        else:
            locals()[arg] = getattr(args, arg)

# get slash style
if sys.platform[0:3] == 'win':
    slashStyle = '\\'
else:
    slashStyle = '/'

# get tables to import
tables = glob.glob(importpath + '/*.ibd')

# get table names
tables = [table.split(slashStyle)[-1].split('.ibd')[0] for table in tables]

# get db connections
if verbose:
    print()
    print('Connecting to MySQL database...')
    print()
dbTarget = MySQLdb.connect(
    host=host,
    user=user,
    passwd=password,
    database=dbname)

if verbose:
    print('Dropping and create new database and tables...')
    print()
# drop existing databaase
cmdDrop = '\"DROP DATABASE IF EXISTS ' + dbname + ';\"'
cmd = 'mysql -u ' + user + ' -p' + password + ' -e ' + cmdDrop
r = os.system(cmd)

# create new target database
cmdCreate = '\"CREATE DATABASE ' + dbname + ' CHARACTER SET utf8 COLLATE utf8_general_ci;\"'
cmd = 'mysql -u ' + user + ' -p' + password + ' -e ' + cmdCreate
r = os.system(cmd)

# create tables
cmd = 'mysql -u ' + user + ' -p' + password + ' ' + dbname + ' < ' + importpath + '/createTables.sql'
r = os.system(cmd)

# loop over tables
if verbose:
    print('Importing data...')
result = quickQuery(dbTarget, 'set foreign_key_checks = 0;')
for table in tables:
    if verbose:
        print('     ' + table)
    # discard table space
    query = 'ALTER TABLE ' + table + ' DISCARD TABLESPACE;'
    result = quickQuery(dbTarget, query)
    # move file
    shutil.copy(importpath + table + '.ibd', datapath + slashStyle + dbname + slashStyle + table + '.ibd')
    # import table space
    query = 'ALTER TABLE ' + table + ' IMPORT TABLESPACE;'
    result = quickQuery(dbTarget, query)
result = quickQuery(dbTarget, 'set foreign_key_checks = 1;')

# close database
if verbose:
    print()
    print('Closing MySQL connection...')
dbTarget.close()


