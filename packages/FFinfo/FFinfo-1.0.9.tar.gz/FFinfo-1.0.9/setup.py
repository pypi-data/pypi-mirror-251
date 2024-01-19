from setuptools import setup, find_packages

setup(
    name='FFinfo',
    version='1.0.9',
    packages=find_packages(),
    install_requires=[
        'requests',
        'python-dotenv',
    ],
)
