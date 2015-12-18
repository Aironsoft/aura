import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_chameleon',
    'pyramid_debugtoolbar',
    'pyramid_tm',
	'pyramid_sacrud',
    'SQLAlchemy',
	'WTForms',
	'webhelpers2',
	'passlib',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    ]

setup(name='aura',
      version='0.0',
      description='aura',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='aura',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = aura:main
      [console_scripts]
      initialize_aura_db = aura.scripts.initializedb:main
      """,
      )
