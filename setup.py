from setuptools import setup
import os

# Load the version from nimbus/__version__.py
version = {}
with open(os.path.join("nimbus", "__version__.py")) as f:
    exec(f.read(), version)

setup(
    name='nimbus-cli',
    version=version['__version__'],
    packages=['nimbus'],
    entry_points={
        'console_scripts': [
            'nimbus=nimbus.__main__:main',
        ],
    },
    author='Your Name',
    description='A simple CLI tool to set up user and web directory for domains.',
    python_requires='>=3.6',
)