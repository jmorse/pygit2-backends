from __future__ import print_function
from pygit2 import Repository as PyGit2Repo
import _pygit2_backends
from _pygit2_backends import open_mysql_backend, create_mysql_backend

supported_repo_attrs = ['TreeBuilder', 'config', 'create_blob', 'create_blob_fromdisk', 'create_blob_fromworkdir', 'create_branch', 'create_commit', 'create_reference', 'create_reference_direct', 'create_reference_symbolic', 'create_tag', 'get', 'git_object_lookup_prefix', 'is_empty', 'listall_branches', 'listall_references', 'lookup_branch', 'lookup_reference', 'merge_base', 'read', 'revparse_single', 'walk', 'write']

class MysqlRepository(PyGit2Repo):
    # XXX XXX XXX dev signature, think some actual thoughts before publishing
    # this API
    def __init__(self, hostname, username, password, dbname, portno, unix_path):
        # Create a struct git_repository hooked up to a mysql backend
        repo = _pygit2_backends.open_mysql_backend(hostname, username,
                                            password, dbname, portno, unix_path)

        # Initialize parent class with given git repo. XXX, exceptions
        super(PyGit2Repo, self).__init__(None, repository_ptr=repo)

    def __getattribute__(self, attr):
        # Remove a ton of Repository object attributes that are out of scope
        # when operating on a custom backend (i.e. the index, working copy,
        # etc). It should be immediately apparent to the developer that these
        # are not supported.

        # First, potentially return an attribute error,
        foo = super(PyGit2Repo, self).__getattribute__(attr)

        # Now filter for things we support
        if attr.startswith('_'):
            return foo
        if attr in supported_repo_attrs:
            return foo

        raise Exception("Attribute \"{0}\" not supported by custom git backends"
                .format(attr))
