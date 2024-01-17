from setuptools import find_packages, setup

setup(
    name='xpt2csv',
    packages=find_packages(include= ['xpt2csv']),
    version='0.1.0',
    description='My first Python library',
    author='Yousuf Ali',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)
