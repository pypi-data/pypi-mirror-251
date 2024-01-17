
from setuptools import setup, find_packages
import os

# Lee el archivo README.md para obtener la descripción larga
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'dynamodb_core', 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="dynamodb-core",
    version="0.2",
    packages=find_packages(include=['dynamodb_core', 'dynamodb_core.test.poc.*']),
    install_requires=[
        "boto3",
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)