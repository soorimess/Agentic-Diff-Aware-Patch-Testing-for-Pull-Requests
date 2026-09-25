# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

import sys
from copy import copy
from unittest.mock import patch

from pylint import modify_sys_path
from pylint.testutils.utils import _test_environ_pythonpath, _test_sys_path


def test_modify_sys_path_only_removes_current_directory_entry() -> None:
    cwd = "/tmp/project"
    default_paths = ["/usr/local/lib/python3.9", "/usr/local/lib/python3.9/site-packages"]
    cases = [
        (["/bundled/packages", *default_paths], ["/bundled/packages", *default_paths]),
        (["", *default_paths], default_paths),
        ([".", *default_paths], default_paths),
        ([cwd, *default_paths], default_paths),
    ]

    with patch("os.getcwd", return_value=cwd):
        for paths, expected_paths in cases:
            with _test_sys_path(copy(paths)), _test_environ_pythonpath():
                modify_sys_path()

                assert sys.path == expected_paths
