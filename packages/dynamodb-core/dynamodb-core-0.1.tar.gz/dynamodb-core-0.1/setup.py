

from setuptools import setup, find_packages

setup(
    name="dynamodb-core",
    version="0.1",
    packages=find_packages(include=['dynamodb_core', 'dynamodb_core.test.poc.*']),
    install_requires=[
        "boto3",
    ],
)



