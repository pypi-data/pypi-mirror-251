from setuptools import setup, find_packages


setup(
    name='mallgo-email',
    version='0.0.8',
    description='mallgo-email',
    author='Inkremental SAS',
    packages=['MallGoEmail'],
    install_requires=[
        'django',
        'requests'
    ],
)