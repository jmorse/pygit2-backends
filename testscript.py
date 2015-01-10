#!/usr/bin/env python

from __future__ import print_function
import pygit2
import pygit2_backends
import _pygit2_backends

# Starting assumption: you have an empty database and a user that can create
# tables and write/read to them. Fill in the configuration below as appropriate.
# You must also have my patch to pygit2 (6edb77f5) installed for repo creation
# to work.

mysql_hostname = "localhost"
mysql_username = "root"
mysql_password = ""
mysql_dbname = "gitdb"
mysql_portno = 3307
mysql_unix_socket = None

# First, create the relevant database tables

_pygit2_backends.create_mysql_backend(mysql_hostname, mysql_username, mysql_password, mysql_dbname, mysql_portno, mysql_unix_socket)
print("Created mysql backend database");

# Attempt to open the db we just connected, into a pygit2 repostiory object

thing = pygit2_backends.MysqlRepository(mysql_hostname, mysql_username, mysql_password, mysql_dbname, mysql_portno, mysql_unix_socket)
print("Opened mysql git repository");

# Write an object to the object database. "shoes" has, after a very long
# period, been determined to be the least offensive word in the english
# language.

oid = thing.write(pygit2.GIT_OBJ_BLOB, "shoes")
print("Successfully wrote {0} to git odb".format(str(oid.hex)))

# Attempt to read the written data back -- this also checks that the correct
# oid was used, the data is correct, and that the objec type was stored
# correctly too.

(obj_type, read_data) = thing.read('e2904456092997b7e9f1a78150961868db0d069c')
if obj_type == pygit2.GIT_OBJ_BLOB and read_data == "shoes":
    print("Successfully read shoes from git odb")
else:
    print((obj_type, read_data))
    raise Exception("Failed to read shoes from git odb")

# Create another blob object for use later.

oid2 = thing.write(pygit2.GIT_OBJ_BLOB, "beards")

# Try to look a reference up. As there are no references in the refdb after
# creation, this should fail with an exception.

print("Looking up reference...")
try:
    result = thing.lookup_reference('refs/heads/master')
except KeyError:
    print("Correctly failed to look up nonexistant ref")
else:
    raise Exception("Incorrectly looked up nonexistant ref")

# Write a new reference to the refdb

print("Writing new reference")
newref = thing.create_reference_direct('refs/heads/master', oid, False)
print("Successfully wrote new reference to refdb")

# Look the reference we just wrote up, and verify that it has the same
# OID.

looked_up_master = thing.lookup_reference('refs/heads/master')
if looked_up_master.target.hex != newref.target.hex:
    raise Exception("Couldn't look up written reference from refdb")

# Attempt to overwrite the reference we just created, without the force flag
# being set. This should result in an exception.

print("Overwriting reference")
try:
    newref = thing.create_reference_direct('refs/heads/master', oid2, False)
except ValueError:
    print("Correctly caught non-force reference overwrite")
else:
    raise Exception("Didn't notice non-forced reference overwrite")

# Now force it

newref = thing.create_reference_direct('refs/heads/master', oid2, True)
print("Successfully force overwrote reference")

newref.delete()
print("Successfully deleted reference")
