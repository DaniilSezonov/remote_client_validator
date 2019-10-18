import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-remote-client-validator',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    description='Simple application for verify remote clients in your API and select template for mail rendering :).',
    long_description=README,
    url='https://github.com/DaniilSezonov',
    author='Daniil Sezonov',
    author_email='sezonov.daniil@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.*',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)