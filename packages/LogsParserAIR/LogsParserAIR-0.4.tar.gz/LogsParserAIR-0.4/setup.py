from setuptools import setup, find_packages

setup(
    name='LogsParserAIR',
    version='0.4',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[ 
        're',
        'collections'
     ]
)