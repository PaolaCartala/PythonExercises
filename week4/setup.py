from setuptools import setup, find_packages

setup(
    name='mytodolists',
    version='1.0',
    author='Paola Cartala',
    author_email='pcartala@applaudiostudios.dev',
    packages=find_packages(exclude=["tests/"]),
)
