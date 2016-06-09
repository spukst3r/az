from setuptools import setup
from az import constants


setup(
    name=constants.PACKAGE_NAME,
    author='spukst3r',
    author_email='spukst3r@gmail.com',
    version='0.1',
    url='https://github.com/spukst3r/az',
    install_requires=[
        'requests>2.9',
        'PyYAML>3.10'
    ],
    packages=['az'],
    entry_points={
        'console_scripts': 'az = az.main:run'
    }
)
