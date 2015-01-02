from pygit2 import Repository as PyGit2Repo

class MysqlRepository(PyGit2Repo):
    def __init__(self, *args, **kwargs):
        # Insert here, mechanism to mangle custom backends into existence
        super(PyGit2Repo, self).__init__(*args, **kwargs)
