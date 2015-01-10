from distutils.core import setup, Extension
import codecs

with codecs.open('README', 'r', 'utf-8') as readme:
        long_description = readme.read()


setup(name="pygit2_backends",
        version="0.0.0",
        author="Jeremy Morse",
        author_email="jmorse+pygit2backends@studentrobotics.org",
        description="Custom backends for use with pylibgit2",
        long_description=long_description,
        license="GPL2",
        # This is extremely unclear. The backends in the backends repo claim
        # to be GPLv2 with linking exception, however libmysqlclient at least
        # is definitely GPL2. Go for the strongest compatible license to
        # reflect this fact.
        packages=['pygit2_backends'],
        ext_modules=[Extension('_pygit2_backends',
            ['src/pygit2_backends.c', 'backends/mysql/mysql.c'],
            include_dirs=['/usr/include/mysql'],
            libraries=['git2', 'mysqlclient'])],
        )
