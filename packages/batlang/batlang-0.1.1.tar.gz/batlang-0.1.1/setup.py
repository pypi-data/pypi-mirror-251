from setuptools import setup

setup(
    name='batlang',
    version='0.1.1',
    packages=['batlang'],
    install_requires=[
        # list your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'bat-lang = batlang.cli:main',
        ],
    },
)
