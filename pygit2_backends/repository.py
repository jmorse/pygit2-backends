from __future__ import print_function
from pygit2 import Repository as PyGit2Repo
import _pygit2_backends
from _pygit2_backends import open_mysql_backend, create_mysql_backend

class MysqlRepository(PyGit2Repo):
    # XXX XXX XXX dev signature, think some actual thoughts before publishing
    # this API
    def __init__(self, hostname, username, password, dbname, portno, unix_path):
        # Create a struct git_repository hooked up to a mysql backend
        repo = _pygit2_backends.open_mysql_backend(hostname, username,
                                            password, dbname, portno, unix_path)

        # Initialize parent class with given git repo. XXX, exceptions
        super(PyGit2Repo, self).__init__(None, repository_ptr=repo)
