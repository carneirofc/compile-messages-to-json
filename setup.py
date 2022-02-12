#!/usr/bin/env python3
import pkg_resources
import typing

from setuptools import setup, find_packages
from src.cpp_msg_to_json import __author__, __version__, __email__


def get_abs_path(relative) -> str:
    return pkg_resources.resource_filename(__name__, relative)


def get_long_description() -> str:
    long_description = ""

    with open(get_abs_path("README.md"), "r") as _f:
        long_description += _f.read().strip()

    long_description += "\n\n"

    with open(get_abs_path("CHANGES.md"), "r") as _f:
        long_description += _f.read().strip()

    return long_description


def get_requirements() -> typing.List[str]:
    with open(get_abs_path("requirements.txt"), "r") as _f:
        return _f.read().strip().split("\n")


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
