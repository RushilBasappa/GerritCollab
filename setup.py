from setuptools import setup

setup(
    name="gere",
    version='0.1',
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        gere=gere:cli
    ''',
)