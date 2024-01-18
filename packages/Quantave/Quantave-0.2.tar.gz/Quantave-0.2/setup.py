# setup.py

from setuptools import setup, find_packages

setup(
    name='Quantave',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        # Add any dependencies here
    ],
    entry_points={
        "console_scripts": [
            "MasterTrainer = QUANTAVE.__master__:proceed"
        ]
    }
)
