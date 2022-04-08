from setuptools import find_packages, setup

"""
To re install:
pip install --editable .

"""
setup(
    name="igpost",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click",
    ],
    entry_points={
        "console_scripts": [
            "igpost = src.scripts.main:cli",
        ],
    },
)
