from distutils.core import setup

setup(name='bowser',
      version='1.1',
      description='urlchecker ',
      author='Pankaj Kumar',
      packages=['bowser'],
      install_requires=['Brotli==1.0.7','bs4==0.0.1','Flask==1.1.2','waitress==2.1.1',
      'httplib2==0.18.1','psycopg2-binary==2.8.5','pycurl==7.43.0.5','requests==2.24.0',
      'SQLAlchemy==1.3.18'],
      entry_points ={'console_scripts': ['bowser = bowser.app:runbowser']}
     )