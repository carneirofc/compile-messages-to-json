#!/usr/bin/env python
import pkg_resources
import typing
import unittest

"""Test suite for cpp_msg_to_json."""

__author__ = "Cláudio Ferreira Carneiro"
__docformat__ = "restructuredtext"


def get_abs_path(relative) -> str:
    return pkg_resources.resource_filename(__name__, relative)


def safe_load(file: str) -> typing.Optional[typing.List[str]]:
    if not pkg_resources.resource_exists(__name__, file):
        return None

    with open(pkg_resources.resource_filename(__name__, file), "r") as f:
        return f.read().strip().split("\n")


class TestTools(unittest.TestCase):
    def test_load_resource(self):
        self.assertIsNone(safe_load("asdasdad"))
        self.assertGreater(safe_load("test_utils/README.md").__le__(), 0)
