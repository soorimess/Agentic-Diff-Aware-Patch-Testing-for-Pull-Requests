import unittest

import pytest
from _pytest.pytester import Pytester


def test_skip_class_tearDown_not_called_with_pdb(pytester: Pytester, monkeypatch) -> None:
    """Regression test for pytest-dev/pytest#10081.

    A unittest.TestCase class decorated with @unittest.skip should not have
    its tearDown() executed when running with --pdb. Previously, --pdb
    could cause tearDown to be executed for skipped classes, leading to errors.
    """
    p = pytester.makepyfile(
        """
        import unittest

        @unittest.skip("skip class")
        class MyTestCase(unittest.TestCase):
            def setUp(self):
                # would raise if executed
                xxx

            def tearDown(self):
                # would raise if executed
                xxx

            def test_one(self):
                pass
        """
    )

    class _DummyPdb:
        quitting = False

        def reset(self):
            pass

        def interaction(self, *args):
            # do not attempt to read from stdin
            pass

    monkeypatch.setattr(
        "_pytest.debugging.pytestPDB._init_pdb", lambda *a, **k: _DummyPdb()
    )

    result = pytester.runpytest_inprocess("--pdb", p)
    # The test should be skipped and not show any NameError from setUp/tearDown.
    result.stdout.fnmatch_lines("* 1 skipped in *")
    assert "NameError" not in "\n".join(result.outlines + result.errlines)
