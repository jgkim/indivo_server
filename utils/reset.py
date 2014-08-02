#!/usr/bin/python

"""
.. module:: utils.reset
   :synopsis: Script for resetting the Indivo Server Database and loading initial data

.. moduleauthor:: Daniel Haas <daniel.haas@post.harvard.edu>

"""

# Set up the Django environment
import sys
import os
from django.core import management
os.environ['DJANGO_SETTINGS_MODULE'] = 'indivo.settings'
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/../'))
from django.db import connection, connections, DatabaseError, IntegrityError

from load_vocabularies import load_vocabularies
from utils.importer import import_data, AppSyncer

from optparse import OptionParser
import subprocess

# Prepare database-specific commands
CONN_DICT = connection.settings_dict
DB_MODULE, DB_NAME = CONN_DICT['ENGINE'].rsplit('.', 1)

# TODO Make the database communications more django like, if not use django to
#       do the setup.

def isvalid(s):
    return type(s) == str and len(s) > 0

if DB_NAME == 'mysql':
    from _mysql_exceptions import OperationalError

    params = []
    if (not isvalid(CONN_DICT['NAME'])):
        raise ValueError("Database setting NAME must be a valid non-empty string")
    if (isvalid(CONN_DICT['USER'])):
        params.append('-u%s' % CONN_DICT['USER'])
    else:
        raise ValueError("Database setting USER must be a valid non-empty string")
    if (isvalid(CONN_DICT['PASSWORD'])):
        params.append('-p%s' % CONN_DICT['PASSWORD'])
    if (isvalid(CONN_DICT['HOST'])):
        params.append('-h %s' % CONN_DICT['HOST'])
    if (isvalid(CONN_DICT['PORT'])):
        params.append('-P %s' % CONN_DICT['PORT'])
    params = " ".join(params)

    CREATE_DB_CMD = 'mysqladmin %s create %s' % (params, CONN_DICT['NAME'])
    DROP_DB_CMD = 'mysqladmin %s drop %s' % (params, CONN_DICT['NAME'])

elif DB_NAME == 'postgresql_psycopg2':
    from psycopg2 import OperationalError
    
    params = []
    if (not isvalid(CONN_DICT['NAME'])):
        raise ValueError("Database setting NAME must be a valid non-empty string")
    if (isvalid(CONN_DICT['USER'])):
        params.append('-U %s' % CONN_DICT['USER'])
    else:
        raise ValueError("Database setting USER must be a valid non-empty string")
    if (isvalid(CONN_DICT['HOST'])):
        params.append('-h %s' % CONN_DICT['HOST'])
    if (isvalid(CONN_DICT['PORT'])):
        params.append('-p %s' % CONN_DICT['PORT'])
    params = " ".join(params)

    CREATE_DB_CMD = 'createdb -W %s %s' % (params, CONN_DICT['NAME'])
    DROP_DB_CMD = 'dropdb -W %s %s' % (params, CONN_DICT['NAME'])

else:
    raise ValueError("Reset Script doesn't support backend %s" % DB_NAME)


def create_db():
    return subprocess.check_call(CREATE_DB_CMD, shell=True)


def drop_db():
    # close django's connection to the database
    connection.close()
    return subprocess.check_call(DROP_DB_CMD, shell=True)

# Parse commandline Arguments
usage = ''' %prog [options]

Reset the Indivo database, optionally loading initial data and vocabularies data. Initial data should
be placed in indivo_server/utils/indivo_data.xml.

Some of the commands (i.e. dropping and creating the database)
require authentication to the underlying database. If you are prompted
for a password, use the password for your database user (the same one you
specified in settings.py)'''

parser = OptionParser(usage=usage)
parser.add_option("-s",
                  action="store_true", dest="syncdb", default=True,
                  help="Reset the Database (default behavior).")
parser.add_option("--no-syncdb",
                  action="store_false", dest="syncdb",
                  help="Don't reset the database.")
parser.add_option("-b",
                  action="store_true", dest="load_data", default=True,
                  help="Load initial data from indivo_data.xml, if available (default behavior).")
parser.add_option("--no-data",
                  action="store_false", dest="load_data",
                  help="Don't load initial data from indivo_data.xml.")
parser.add_option("-c",
                  action="store_true", dest="load_vocabularies", default=False,
                  help="Load vocabularies data, if available.")
parser.add_option("--no-vocabularies",
                  action="store_false", dest="load_vocabularies",
                  help="Don't load vocabularies data (default behavior).")
parser.add_option("--force-drop",
                  action="store_true", dest="force_drop", default=False,
                  help="Force a drop and recreate of the database (useful if flushing the database fails).")
parser.add_option("--no-force-drop",
                  action="store_false", dest="force_drop",
                  help="Don't force a drop and recreate of the database unless necessary (default behavior).")

(options, args) = parser.parse_args()

# Prompt for confirmation--we are about to trash a database, after all
confirm = raw_input("""You have requested a reset of the database.
This will IRREVERSIBLY DESTROY all data currently in the %r database,
and return each table to its initial state.
Are you sure you want to do this?

    Type 'yes' to continue, or 'no' to cancel: """ % CONN_DICT['NAME'])

if confirm != 'yes':
    print "Reset Cancelled."

else:

    # Reset the Database
    if options.syncdb:
        print "RESETTING DATABASE..."

        # Assume the database exists and is synced: try flushing the database
        force_drop = options.force_drop
        if not force_drop:
            try:
                print "Flushing the Database of existing data..."
                management.call_command('flush', verbosity=0, interactive=False)
                # TODO: Support for multiple databases
                management.call_command('flush', database='vocabularies', verbosity=0, interactive=False)
                management.call_command('migrate', fake=True, verbosity=0)
                print "Database Flushed."

            # Couldn't flush. Either the database doesn't exist, or it is corrupted.
            # Try dropping and recreating, below
            except (OperationalError, DatabaseError, IntegrityError) as e:
                force_drop = True

            # Unknown exception. For now, just treat same as other exceptions
            except Exception as e:
                force_drop = True

        if force_drop:

            # Try dropping the database, in case it existed
            print "Database nonexistent or corrupted, or Database drop requeseted. Attempting to drop database..."
            try:
                drop_db()

                # TODO: Support for multiple databases
                connections['vocabularies'].close()
                CONN_DICT = connections['vocabularies'].settings_dict
                params = []
                if (not isvalid(CONN_DICT['NAME'])):
                    raise ValueError("Database setting NAME must be a valid non-empty string")
                if (isvalid(CONN_DICT['USER'])):
                    params.append('-u %s' % CONN_DICT['USER'])
                else:
                    raise ValueError("Database setting USER must be a valid non-empty string")
                if (isvalid(CONN_DICT['PASSWORD'])):
                    params.append('-p %s' % CONN_DICT['PASSWORD'])
                else:
                    raise ValueError("Database setting PASSWORD must be a valid non-empty string")
                if (isvalid(CONN_DICT['HOST'])):
                    params.append('--host %s' % CONN_DICT['HOST'])
                if (isvalid(CONN_DICT['PORT'])):
                    params.append('--port %s' % CONN_DICT['PORT'])
                params = " ".join(params)
                subprocess.check_call('mongo %s --eval "db.dropDatabase()" %s' % (params, CONN_DICT['NAME']), shell=True, stdout=open('/dev/null', 'w'))
            except subprocess.CalledProcessError:
                print "Couldn't drop database. Probably because it didn't exist."

            # Create the Database
            print "Creating the Database..."
            try:
                create_db()
            except subprocess.CalledProcessError:
                print "Couldn't create database. Database state likely corrupted. Exiting..."
                exit()

            # Sync the Database
            print "Syncing and Migrating the database..."
            management.call_command('syncdb', verbosity=0)
            # TODO: Support for multiple databases
            management.call_command('syncdb', database='vocabularies', verbosity=0)

            # Migrate the Database
            management.call_command('migrate', verbosity=0)
            print "Database Synced."

    # Load vocabularies
    if options.load_vocabularies:
        print "LOADING VOCABULARIES DATA..."
        try:
            load_vocabularies()
            print "LOADED."
        except Exception as e:
            print str(e)
            print "COULDN'T LOAD DATA. SKIPPING."

    # Import initial data
    if options.load_data:
        print "LOADING INITIAL INDIVO DATA..."
        try:
            import_data()
            AppSyncer().sync()
            print "LOADED."
        except Exception as e:
            print str(e)
            print "COULDN'T LOAD DATA. SKIPPING."
