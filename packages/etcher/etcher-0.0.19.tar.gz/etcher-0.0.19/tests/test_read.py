import json
import os
import re
import typing as tp
from unittest import mock

import pytest

from .helpers import cli
from .helpers.tmp_file_manager import TmpFileManager
from .helpers.utils import check_single

# Define a sample TOML file for testing
sample_toml = """
[info]
  name = "John"
  age = 30

[colors]
  primary = "blue"
  secondary = "green"

[fruits]
  list = ["apple", "orange", "banana"]
"""


def run_read(toml: str, path: str, is_json=False) -> str:
    """Run the read subcommand on the given TOML file and path."""
    with TmpFileManager() as manager:
        return cli.run(
            [
                "etch",
                "read",
                path,
                "--config",
                str(manager.tmpfile(toml)),
            ]
            + (["--output", "json"] if is_json else [])
        )


@pytest.mark.parametrize(
    "path, expected_json_result, custom_expected_raw_result",
    [
        # Full:
        (
            "",
            {
                "info": {"name": "John", "age": 30},
                "colors": {"primary": "blue", "secondary": "green"},
                "fruits": {"list": ["apple", "orange", "banana"]},
            },
            None,
        ),
        # Table:
        ("info", {"name": "John", "age": 30}, None),
        # Int:
        ("info.age", 30, None),
        # Str:
        (
            "colors.primary",
            "blue",
            "blue",
        ),  # With raw and json this is different, because json comes out as '"json"' whereas raw shouldn't wrap in quotes.
        # Arr:
        ("fruits.list", ["apple", "orange", "banana"], None),
        ("fruits.list.1", "orange", "orange"),  # Same here with the raw difference
    ],
)
def test_read_working(
    path: str, expected_json_result: tp.Any, custom_expected_raw_result: tp.Optional[str]
):
    json_result = json.loads(run_read(sample_toml, path, is_json=True))
    assert json_result == expected_json_result
    raw_result = run_read(sample_toml, path)
    if custom_expected_raw_result is None:
        assert json.loads(raw_result) == expected_json_result
    else:
        assert raw_result == custom_expected_raw_result


def test_read_as_input_to_env():
    """Confirm the use case of reading the default, and writing it to the env to use on a run (when ban-defaults is used) works fine."""
    config = """
[context.env]
  MY_TEST_VAR = { default = "Hello" }
"""
    with TmpFileManager() as manager:
        read_val = run_read(config, "context.env.MY_TEST_VAR.default")
        with mock.patch.dict(
            os.environ,
            {
                "MY_TEST_VAR": read_val,
            },
        ):
            check_single(
                manager,
                manager.tmpfile(config),
                "{{ MY_TEST_VAR }}!",
                "Hello!",
            )


@pytest.mark.parametrize(
    "path, error_message",
    [
        (
            "nonexistent",
            "Failed to read toml path: 'nonexistent'. Failed at: 'root' with error: 'Key 'nonexistent' not found in active table. Avail keys: 'colors, fruits, info'.'",
        ),
        (
            "colors.nonexistent",
            "Failed to read toml path: 'colors.nonexistent'. Failed at: 'colors' with error: 'Key 'nonexistent' not found in active table. Avail keys: 'primary, secondary'.'",
        ),
        (
            "fruits.list.5",
            "Failed to read toml path: 'fruits.list.5'. Failed at: 'fruits.list' with error: 'Index '5' is outside the bounds of the array (len 3).",
        ),
        (
            "fruits.list.-1",
            "Failed to read toml path: 'fruits.list.-1'. Failed at: 'fruits.list' with error: 'Table key '-1' cannot be found. Active element is an array.",
        ),
    ],
)
def test_read_fail(path, error_message):
    with pytest.raises(ValueError, match=re.escape(error_message)):
        run_read(sample_toml, path)
