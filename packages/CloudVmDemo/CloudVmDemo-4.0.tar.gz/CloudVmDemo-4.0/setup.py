from setuptools import setup, find_packages

setup(
    name='CloudVmDemo',
    version='4.0',
    description='eNlight Cloud VM create, update, retrive, delete and VM actions',
    author='Akshay Ghatol',
    author_email='akshay.ghatol@esds.co.in',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
)

