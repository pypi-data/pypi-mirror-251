from setuptools import setup, find_namespace_packages
from db_email.version import Version


setup(name='django-db-email',
     version=Version('1.0.0').number,
     description='Db backend for Django mails',
     long_description=open('README.md').read().strip(),
     long_description_content_type="text/markdown",
     author='Bram Boogaard',
     author_email='padawan@hetnet.nl',
     url='https://github.com/bboogaard/django-db-email',
     packages=find_namespace_packages(
         include=[
             'db_email',
             'db_email.migrations'
         ]
     ),
     include_package_data=True,
     install_requires=[
         'django~=4.2.7',
     ],
     license='MIT License',
     zip_safe=False,
     keywords='Django Email Backend',
     classifiers=['Development Status :: 3 - Alpha'])
