from setuptools import setup, find_namespace_packages

setup(
    name='pycentroid-common',
    packages=find_namespace_packages(include=['centroid.*'])
)