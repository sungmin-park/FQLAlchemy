from setuptools import setup

setup(
    name='FQLalchemy',
    version='0.0.1',
    packages=['fqlalchemy'],
    install_requires=['sqlalchemy>=0.8', 'simplejson'],
    entry_points={
        'sqlalchemy.dialects': ['fql = fqlalchemy.dialect:FQLDialect'],
    },
)
