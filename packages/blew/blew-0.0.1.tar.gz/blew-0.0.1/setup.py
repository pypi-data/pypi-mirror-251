from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="blew",
    version="0.0.1",
    description="ai in development",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/blew/blew",
    author="blew",
    author_email="blew.ai@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    #install_requires=["blew-core"],
    entry_points={
        "console_scripts": [
            "blew = blew.main:main",
        ],
    },
)