#!/usr/bin/env python3
import os
import pkg_resources
import typing

from setuptools import setup, find_packages
from src.cpp_msg_to_json import __author__, __version__, __email__


def safe_load(file: str) -> str:
    if not os.path.isfile(file):
        return ""

    with open(pkg_resources.resource_filename(__name__, file), "r") as f:
        return f.read().strip()


def get_long_description() -> str:
    long_description = ""

    long_description += safe_load("README.md")

    long_description += "\n\n"

    long_description += safe_load("CHANGES.md")

    return long_description


def get_requirements() -> typing.List[str]:
    return safe_load("requirements.txt").split("\n")


def main():
    long_description = get_long_description()

    requirements = get_requirements()

    setup(
        author=__author__,
        author_email=__email__,
        classifiers=[
            "Programming Language :: Python :: 3",
        ],
        description="Parse c/c++ compile messages into json",
        download_url="https://github.com/carneirofc/cpp_msg_to_json",
        license="GLPv3",
        long_description=long_description,
        long_description_content_type="text/markdown",
        name="cpp_msg_to_json",
        url="https://github.com/carneirofc/cpp_msg_to_json",
        version=__version__,
        install_requires=requirements,
        include_package_data=True,
        packages=find_packages(
            where="src",
            include=[
                "cpp_msg_to_json*",
            ],
        ),
        package_dir={"": "src"},
        python_requires=">=3.6",
        scripts=[],
        zip_safe=False,
    )


if __name__ == "__main__":
    main()
