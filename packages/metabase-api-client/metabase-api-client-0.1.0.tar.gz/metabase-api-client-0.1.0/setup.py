from setuptools import setup, find_packages

setup(
    name='metabase-api-client',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'multischema-metabase-dashboard-helper=metabase_api.main:main',
        ],
    },
)
