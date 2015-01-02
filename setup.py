from distutils.core import setup, Extension
import codecs

with codecs.open('README', 'r', 'utf-8') as readme:
        long_description = readme.read()


setup(name="pygit2-backends",
        version="0.0.0",
        author="Jeremy Morse",
        author_email="jmorse+pygit2backends@studentrobotics.org",
        description="Custom backends for use with pylibgit2",
        long_description=long_description,
        license="GPL2 with linking exception",
        #packages=['pygit2-backends'],
        ext_modules=[Extension('_pygit2-backends',
            ['backends/mysql/mysql.c'])],
        )
