from setuptools import setup, find_packages 
  
setup( 
    name='sbomgencli', 
    version='1.0.0', 
    description='CLI tool for sbomgen', 
    author='cd dev', 
    author_email='akashsah2003@gmail.com', 
    packages=['sbomgencli', 
            'sbomgencli.Parsers', 
            'sbomgencli.Utility'
            ], 
    install_requires=[ 
        'datetime',
        'argparse',
        'toml',
        'dicttoxml'
    ],
    entry_points= {
        'console_scripts': [
            'sbomgen = sbomgencli.main:main',
        ],
    },
) 