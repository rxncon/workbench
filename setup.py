import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='rxncon_GUI',
    scripts=[
        'runserver.py'
    ],
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',  # example license
    description='A browser based interface for the rxncon framework.',
    long_description=README,
    url='https://www.rxncon.org/',
    author='Mathias Wajnberg',
    author_email='mathias.wajnberg@hu-berlin.de',
    keywords=['sysbio', 'signalling', 'systems biology'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10.4', 
        'Intended Audience :: sys bio',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'django',
	'rxncon',
	'typecheck-decorator',
        'typing',
        'xlrd',
    ]
)
