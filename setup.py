import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid>=1.0',
    'SQLAlchemy',
    'transaction',
    'repoze.tm2',
    'zope.sqlalchemy',
    'WebError',
    ]

if sys.version_info[:3] < (2,5,0):
    requires.append('pysqlite')

setup(name='formalchemy_project',
      version='0.0',
      description='formalchemy_project',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      message_extractors = { 'formalchemy_project': [
             ('*.py',   'lingua_python', None ),
             ('templates/**.pt',   'lingua_xml', None ),
             ]},
      zip_safe=False,
      test_suite='formalchemy_project',
      install_requires = requires,
      entry_points = """\
      [paste.app_factory]
      main = formalchemy_project:main
      bootstrap = formalchemy_project.fa_bootstrap:main
      """,
      paster_plugins=['pyramid'],
      )

