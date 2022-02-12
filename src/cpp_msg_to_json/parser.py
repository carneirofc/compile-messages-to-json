#!/usr/bin/env python
import argparse
import dataclasses
import os
import re
import sys
import json
import typing

level_mapping = {"debug": 0, "trace": 0, "info": 1, "warning": 2, "error": 3}


@dataclasses.dataclass(frozen=True)
class Finding:
    file: str
    line: int
    col: int
    level: str
    message: str
    checks: str

    def __gt__(self, other):
        if self.file != other.file:
            return self.file > other.file

        if self.line != other.line:
            return self.line > other.line

        if self.col != other.col:
            return self.col > other.col

        return level_mapping.get(self.level, -1) > level_mapping.get(other.level, -1)


def create_finding(data):
    if not data or type(data) != tuple or len(data) != 6:
        raise ValueError("Invalid input {}".format(data))
    file, line, col, level, message, checks = data
    return Finding(
        file=str(file),
        line=int(line),
        col=int(col),
        level=level,
        message=message,
        checks=checks,
    )


class Processor:
    def process(self, line: str):
        raise NotImplementedError()


class GnuCxxProcessor(Processor):
    _gcc_info_re = re.compile(r"^(.*?):(\d+):(\d+):\s(warning|info|error):\s(.*)$")

    def process(self, line: str):
        match = self._gcc_info_re.search(line)

        if not match or match.lastindex != 5:
            # ignore invalid
            return
        file, line, col, level, message = match.groups()

        return (file, line, col, level, message, "")


class ClangTidyProcessor(Processor):
    _clang_info_re = re.compile(
        r"^(.*?):(\d+):(\d+):\s(warning|info|error):\s(.*) \[(.*)\]$"
    )

    def process(self, line: str):
        match = self._clang_info_re.search(line)

        if not match or match.lastindex != 6:
            # ignore invalid
            return
        file, line, col, level, message, checks = match.groups()

        return (file, line, col, level, message, checks)


class Findings:
    _findings: typing.List[Finding] = []

    def add(self, data):
        if not data:
            return

        self._findings.append(create_finding(data))

    def to_dict(self):
        ret = set()
        for f in self._findings:
            ret.add(f)

        _list = list(ret)
        _list.sort()
        return [d.__dict__ for d in _list]


class Reader:
    def data(self):
        raise NotImplementedError()


class FileReader(Reader):
    def __init__(self, file: str):
        super().__init__()

        if not file or not os.path.isfile(file):
            raise ValueError("Invalid file name '{}'".format(file))

        self._file = file

    def data(self):
        with open(self._file, "r") as f:
            for line in f:
                yield line


class StdinReader(Reader):
    def data(self):
        for line in sys.stdin:
            yield line


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, default=None, required=False, dest="file")
    parser.add_argument(
        "--type", choices=["clang-tidy", "gxx"], default="clang-tidy", dest="type"
    )
    parser.add_argument(
        "--out", type=str, default="output.json", required=False, dest="out"
    )

    args = parser.parse_args()

    reader = FileReader(args.file) if args.file else StdinReader()
    findings = Findings()
    processor = ClangTidyProcessor() if args.type == "clang-tidy" else GnuCxxProcessor()

    for line in reader.data():
        findings.add(processor.process(line))
        sys.stdout.write(line)

    with open(args.out, "w+") as f:
        json.dump(findings.to_dict(), f, indent=2)
