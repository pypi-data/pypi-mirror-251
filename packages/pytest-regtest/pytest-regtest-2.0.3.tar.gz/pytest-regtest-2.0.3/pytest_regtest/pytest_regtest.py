import difflib
import functools
import inspect
import os
import re
import sys
import tempfile
from hashlib import sha512
from io import StringIO

import pytest
from _pytest._code.code import TerminalRepr
from _pytest._io import TerminalWriter

pytest_plugins = ["pytester"]

IS_WIN = sys.platform == "win32"


def ljust(s, *a):
    return s.ljust(*a)


class RegtestException(Exception):
    pass


def pytest_addoption(parser):
    """Add options to control the timeout plugin"""
    group = parser.getgroup("regtest", "regression test plugin")
    group.addoption(
        "--regtest-reset",
        action="store_true",
        help="do not run regtest but record current output",
    )
    group.addoption(
        "--regtest-tee",
        action="store_true",
        default=False,
        help="print recorded results to console too",
    )
    group.addoption(
        "--regtest-consider-line-endings",
        action="store_true",
        default=False,
        help="do not strip whitespaces at end of recorded lines",
    )
    group.addoption(
        "--regtest-nodiff",
        action="store_true",
        default=False,
        help="do not show diff output for failed regresson tests",
    )


def pytest_configure(config):
    config.pluginmanager.register(PytestRegtestPlugin())


class PytestRegtestPlugin:
    def __init__(self):
        self._reset_regtest_outputs = []
        self._failed_regtests = []

    @pytest.hookimpl(trylast=True)
    def pytest_runtest_call(self, item):
        if hasattr(item, "regtest_stream"):
            self.check_recorded_output(item)

    def check_recorded_output(self, item):
        test_folder = item.fspath.dirname
        regtest_stream = item.regtest_stream
        identifier = regtest_stream.identifier

        recorded_output_path = result_file_path(test_folder, item.nodeid, identifier)

        config = item.config

        ignore_line_endings = not config.getvalue("--regtest-consider-line-endings")
        reset = config.getvalue("--regtest-reset")

        if reset:
            os.makedirs(os.path.dirname(recorded_output_path), exist_ok=True)
            with open(recorded_output_path, "w", encoding="utf-8") as fh:
                fh.write("".join(regtest_stream.get_lines()))
            self._reset_regtest_outputs.append(recorded_output_path)
            return

        if os.path.exists(recorded_output_path):
            with open(recorded_output_path, "r", encoding="utf-8") as fh:
                tobe = fh.readlines()
        else:
            tobe = []

        current = regtest_stream.get_lines()
        if ignore_line_endings:
            current = [line.rstrip() for line in current]
            tobe = [line.rstrip() for line in tobe]

        if current != tobe:
            self._failed_regtests.append(item)
            raise RegtestException(current, tobe, regtest_stream)

    @pytest.hookimpl(hookwrapper=True)
    def pytest_pyfunc_call(self, pyfuncitem):
        stdout = sys.stdout
        if "regtest_all" in pyfuncitem.fixturenames and hasattr(
            pyfuncitem, "regtest_stream"
        ):
            sys.stdout = pyfuncitem.regtest_stream
        yield
        sys.stdout = stdout

    @pytest.hookimpl(hookwrapper=True)
    def pytest_report_teststatus(self, report, config):
        outcome = yield
        if report.when == "call":
            if config.getvalue("--regtest-reset"):
                result = outcome.get_result()
                if result[0] != "failed":
                    outcome.force_result((result[0], "R", "RESET"))

    def pytest_terminal_summary(self, terminalreporter, exitstatus, config):
        terminalreporter.ensure_newline()
        terminalreporter.section("pytest-regtest report", sep="-", blue=True, bold=True)
        terminalreporter.write("total number of failed regression tests: ", bold=True)
        terminalreporter.line(str(len(self._failed_regtests)))
        if config.getvalue("--regtest-reset"):
            if config.option.verbose:
                terminalreporter.line(
                    "the following output files have been reset:", bold=True
                )
                for path in self._reset_regtest_outputs:
                    rel_path = os.path.relpath(path)
                    terminalreporter.line("  " + rel_path)
            else:
                terminalreporter.write(
                    "total number of reset output files: ", bold=True
                )
                terminalreporter.line(str(len(self._reset_regtest_outputs)))

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        outcome = yield
        if call.when == "teardown" and hasattr(item, "regtest_stream"):
            if item.config.getvalue("--regtest-tee"):
                tw = TerminalWriter()
                tw.line()
                line = "recorded raw output to regtest fixture: "
                line = ljust(line, tw.fullwidth, "-")
                tw.line(line, green=True)
                tw.write(item.regtest_stream.get_output() + "\n", cyan=True)
                tw.line("-" * tw.fullwidth, green=True)
                tw.line()
                tw.flush()

                test_folder = item.fspath.dirname
                regtest_stream = item.regtest_stream
                identifier = regtest_stream.identifier

                recorded_output_path = result_file_path(
                    test_folder, item.nodeid, identifier
                )
                result = outcome.get_result()
                result.longrepr = CollectErrorRepr(
                    [f"wrote recorded output to {recorded_output_path}"], [dict()]
                )
                return

        if call.when != "call" or not hasattr(item, "regtest_stream"):
            return

        if call.excinfo is not None and call.excinfo.type is RegtestException:
            current, recorded, regtest_stream = call.excinfo.value.args

            nodeid = item.nodeid + (
                ""
                if regtest_stream.identifier is None
                else "__" + regtest_stream.identifier
            )

            nodiff = item.config.getvalue("--regtest-nodiff")
            ignore_line_endings = not item.config.getvalue(
                "--regtest-consider-line-endings"
            )

            result = outcome.get_result()

            if not ignore_line_endings:
                # add quotes around lines in diff:

                current = list(map(repr, current))
                recorded = list(map(repr, recorded))

            collected = list(
                difflib.unified_diff(current, recorded, "is", "tobe", lineterm="")
            )

            msg = "\nregression test output differences for {}:\n".format(nodeid)
            if nodiff:
                msg_diff = f"{len(collected)} lines in diff"
            else:
                msg_diff = ">   " + "\n>   ".join(collected)

            result.longrepr = CollectErrorRepr(
                [msg, msg_diff + "\n"], [dict(), dict(red=True, bold=True)]
            )


def result_file_path(test_folder, nodeid, identifier):
    file_name, __, test_function = nodeid.partition("::")
    file_name = os.path.basename(file_name)

    for c in "/\\:*\"'?<>|":
        test_function = test_function.replace(c, "-")

    # If file name is too long, hash parameters.
    if len(test_function) > 100:
        test_function = (
            test_function[:88]
            + "__"
            + sha512(test_function.encode("utf-8")).hexdigest()[:10]
        )

    test_function = test_function.replace(" ", "_")
    stem, __ = os.path.splitext(file_name)
    if identifier is not None:
        output_file_name = stem + "." + test_function + "__" + identifier + ".out"
    else:
        output_file_name = stem + "." + test_function + ".out"

    return os.path.join(test_folder, "_regtest_outputs", output_file_name)


@pytest.fixture
def regtest(request):
    yield RegtestStream(request)


@pytest.fixture
def regtest_all(regtest):
    yield regtest


class RegtestStream:
    def __init__(self, request):
        request.node.regtest_stream = self
        self.request = request
        self.buffer = StringIO()
        self.identifier = None

    def write(self, what):
        self.buffer.write(what)

    def flush(self):
        pass

    def get_lines(self):
        output = self.buffer.getvalue()
        if not output:
            return []
        output = cleanup(output, self.request)
        lines = output.splitlines(keepends=True)
        return lines

    def get_output(self):
        return self.buffer.getvalue()

    def __enter__(self):
        sys.stdout = self
        return self

    def __exit__(self, *a):
        sys.stdout = sys.__stdout__
        return False  # dont suppress exception


def cleanup(output, request):
    for converter in _converters_pre:
        output = converter(output, request)

    output = _std_conversion(output, request)

    for converter in _converters_post:
        output = converter(output, request)

    # in python 3 a string should not contain binary symbols...:
    if contains_binary(output):
        request.raiseerror(
            "recorded output for regression test contains unprintable characters."
        )

    return output


# the function below is modified version of http://stackoverflow.com/questions/898669/
textchars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7F})


def contains_binary(txt):
    return bool(txt.translate(dict(zip(textchars, " " * 9999))).replace(" ", ""))


_converters_pre = []
_converters_post = []


def _fix_pre_v2_converter_function(function):
    @functools.wraps(function)
    def fixed_converter_function(output, request):
        return function(output)

    return fixed_converter_function


def register_converter_pre(function):
    if function not in _converters_pre:
        signature = inspect.signature(function)
        # keep downward compatibility:
        if len(signature.parameters) == 1:
            function = _fix_pre_v2_converter_function(function)
        _converters_pre.append(function)


def register_converter_post(function):
    if function not in _converters_post:
        signature = inspect.signature(function)
        # keep downward compatibility:
        if len(signature.parameters) == 1:
            function = _fix_pre_v2_converter_function(function)
        _converters_post.append(function)


def _std_replacements(request):
    if "tmpdir" in request.fixturenames:
        tmpdir = request.getfixturevalue("tmpdir").strpath + os.path.sep
        yield tmpdir, "<tmpdir_from_fixture>/"
        tmpdir = request.getfixturevalue("tmpdir").strpath
        yield tmpdir, "<tmpdir_from_fixture>"

    regexp = os.path.join(
        os.path.realpath(tempfile.gettempdir()), "pytest-of-.*", r"pytest-\d+/"
    )
    yield regexp, "<pytest_tempdir>/"

    regexp = os.path.join(tempfile.gettempdir(), "tmp[_a-zA-Z0-9]+")

    yield regexp, "<tmpdir_from_tempfile_module>"
    yield os.path.realpath(
        tempfile.gettempdir()
    ) + os.path.sep, "<tmpdir_from_tempfile_module>/"
    yield os.path.realpath(tempfile.gettempdir()), "<tmpdir_from_tempfile_module>"
    yield tempfile.tempdir + os.path.sep, "<tmpdir_from_tempfile_module>/"
    yield tempfile.tempdir, "<tmpdir_from_tempfile_module>"
    yield r"var/folders/.*/pytest-of.*/", "<pytest_tempdir>/"

    # replace hex object ids in output by 0x?????????
    yield r" 0x[0-9a-fA-F]+", " 0x?????????"


def _std_conversion(output, request):
    fixed = []
    for line in output.splitlines(keepends=True):
        for regex, replacement in _std_replacements(request):
            if IS_WIN:
                # fix windows backwards slashes in regex
                regex = regex.replace("\\", "\\\\")
            line, __ = re.subn(regex, replacement, line)
        fixed.append(line)
    return "".join(fixed)


class CollectErrorRepr(TerminalRepr):
    def __init__(self, messages, colors):
        self.messages = messages
        self.colors = colors

    def toterminal(self, out):
        for message, color in zip(self.messages, self.colors):
            out.line(message, **color)
