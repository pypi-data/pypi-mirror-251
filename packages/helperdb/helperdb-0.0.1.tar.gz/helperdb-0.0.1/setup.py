from setuptools import setup, find_packages

setup(
    name="helperdb",
    version="0.0.1",
    description="A database system for discord bots",
    packages=find_packages(),
    install_requires=[
        "aiosqlite"
    ]
)
