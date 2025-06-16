from setuptools import setup

setup(
    name='nimbus-cli',
    version='0.7',
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