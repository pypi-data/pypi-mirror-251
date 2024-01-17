from setuptools import setup, find_packages

setup(
    name='translatifyplux',
    version='0.3',
    description='A translation library for TSA API',
    author='Uncover',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
)
