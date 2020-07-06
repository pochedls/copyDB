#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Stephen Po-Chedley 5 July 2020

This is the export script as part of copyDB. It is intended to
export a MySQL database (which can then be read-in with an import
script). It will:
    1) copy all of the MySQL tables for the source database to an
       export folder
    2) produce a createTable.sql script to create all the tables
       in the source database

Parameters can be specified via the config.py file or via the command line.
The arguments needed (in config.py) are:
    * source_dbname       : source database to be exported
    * source_user         : user of source database
    * source_password     : user password for source database
    * source_host         : host for source database
    * source_datapath     : path to underlining database files
    * source_export       : location to copy export data

Alternatively, these can be specifed via command line arguments (see help):
    ./export.py --help

The environment was created / implemented using:
    conda create -n copydb mysql-connector-python mysqlclient ipython python=3
    conda activate copydb

Alternatively, these packages can be installed with pip.

@author: pochedls
"""

# package / function imports
import config
from fx import quickQuery
from fx import quickWrite
from fx import str2bool
import glob
import shutil
import os
import MySQLdb
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
                        help="Source database name")

    parser.add_argument('-u', '--user', type=str,
                        help="MySQL username for source database")

    parser.add_argument('-p', '--password', type=str,
                        help="MySQL user password for source database")

    parser.add_argument('-c', '--host', type=str,
                        help="MySQL host (e.g., localhost) for source " +
                        "database")

    parser.add_argument('-dp', '--datapath', type=str,
                        help="Path to MySQL database files " +
                        "(e.g., /usr/local/var/mysql/)")

    parser.add_argument('-e', '--export', type=str,
                        help="Path to export source database (e.g., export/)")

    # override any config options with command line options
    args = parser.parse_args()

    verbose = args.verbose
    for arg in vars(args):
        if getattr(args, arg) is None:
            locals()[arg] = getattr(config, 'source_' + arg)
        else:
            locals()[arg] = getattr(args, arg)

# specify table export filename
fnTables = export + '/createTables.sql'

# if export directory does not exist, make it
if not os.path.exists(export):
    os.mkdir(export)

# get list of tables
tables = glob.glob(datapath + '/' + dbname + '/*.ibd')

# get table names
tables = [table.split('/')[-1].split('.ibd')[0] for table in tables]

# get db connections
if verbose:
    print()
    print('Connecting to MySQL database...')
    print()
dbSource = MySQLdb.connect(
    host=host,
    user=user,
    passwd=password,
    database=dbname)

# if table export exists, remove it
if os.path.exists(fnTables):
    if verbose:
        print('Dropping old table export...')
        print()
    os.remove(fnTables)
# remove foreign key constraint in table export script
quickWrite(fnTables, 'set foreign_key_checks = 0;')

# loop over tables
if verbose:
    print('Creating export...')
for table in tables:
    if verbose:
        print('     ' + table)
    # get create table syntax and write to table export script
    query = 'SHOW CREATE TABLE `' + table + '`;'
    result = quickQuery(dbSource, query)
    quickWrite(fnTables, result[0][1] + ';')
    # export and move table backup to export directory
    query = 'FLUSH TABLE ' + table + ' FOR EXPORT;'
    result = quickQuery(dbSource, query)
    shutil.copy(datapath + '/' + dbname + '/' + table + '.ibd', export)
    # unlock database
    query = 'UNLOCK TABLES;'
    result = quickQuery(dbSource, query)
# add foreign key constraint in table export script
quickWrite(fnTables, 'set foreign_key_checks = 1;')

if verbose:
    print()
    print('Closing MySQL connection...')
# close database
dbSource.close()
