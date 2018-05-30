import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='rxncon_workbench',
    scripts=[
        'rxncon_workbench.py'
    ],
    version='0.97',
    packages=find_packages(),
    packages_dir={'media_cdn': 'media_cdn/'},
    package_data={'media_cdn': ['hog-example/Table_S1_Hog1_acyclic_reconstruction.xls']},
    include_package_data=True,
    license='LGPL License', 
    description='A browser based interface for the rxncon framework.',
    long_description=README,
    url='https://www.rxncon.org/',
    author='Mathias Wajnberg',
    author_email='mathiasw224@yahoo.de',
    keywords=['sysbio', 'signalling', 'systems biology'],
    install_requires=[
        'django==1.10.4',
        'rxncon==2.0b17',],
    # data_files=[
    #     ('media_cdn/hog-example/boolnet', ['media_cdn/hog-example/boolnet/hog-example_initial_vals.csv']),
    #     ('media_cdn/hog-example/boolnet', ['media_cdn/hog-example/boolnet/hog-example_model.boolnet']),
    #     ('media_cdn/hog-example/boolnet', ['media_cdn/hog-example/boolnet/hog-example_symbols.csv']),
    #     ('media_cdn/hog-example/graphs',  ["media_cdn/hog-example/graphs/hog-example_Table_S1_Hog1_acyclic_reconstruction_reaGraph.xgmml"]),
    #     ('media_cdn/hog-example/', ['media_cdn/hog-example/Table_S1_Hog1_acyclic_reconstruction.xls']),
    #
    #     ('media_cdn/hog-example-text-format/description', ['media_cdn/hog-example-text-format/description/hog-example-text-format_quick_definition.txt']),
    #     ('media_cdn/hog-example-text-format/graphs', ['media_cdn/hog-example-text-format/graphs/hog-example-text-format_HOG Example text format_sReaGraph.xgmml']),
    #     ('media_cdn/hog-example-text-format/rule_based', ['media_cdn/hog-example-text-format/rule_based/hog-example-text-format_model.bngl']),
    # ],

)
