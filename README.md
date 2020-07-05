# copyDB

Python functionality to copy database using transportable tablespaces. Includes `export.py` to 
export tables of an existing database and `import.py` to import that data into a new database.

## Setup

### Create conda environment

    conda create -n sql mysql-connector-python mysqlclient ipython python=3
    conda activate sql

### Update config file

* Rename `configTemplate.py` to `config.py`
* Update arguments in `config.py` to correspond to correct MySQL database

## Run export / import

    python export.py
    python import.py

## Other notes

* Not sure if I need to do something with .cfg files
* This setup was replicated from a blog about [transportable table space](https://blog.toadworld.com/2017/06/14/transportable-tablespaces-in-innodb)
* Ideally export would be run nightly on production to produce export files and there would be an intermediate (yet to be written) script to rsync the remote export to the local import directory
