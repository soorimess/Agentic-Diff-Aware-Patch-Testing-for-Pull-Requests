import pytest
from _pytest.monkeypatch import MonkeyPatch


def test_pdb_teardown_skipped_class(pytester: pytest.Pytester, monkeypatch: MonkeyPatch) -> None:
    """With --pdb, setUp and tearDown should not be called for classes decorated with unittest.skip.

    Regression test for pytest-dev/pytest#10081: previously tearDown() could be executed for
    classes marked with @unittest.skip when running with --pdb.
    """
    tracked = []
    # expose the tracking list to the test module via the pytest module
    monkeypatch.setattr(pytest, "pdb_teardown_skipped_class", tracked, raising=False)

    pytester.makepyfile(
        """
        import unittest
        import pytest

        @unittest.skip("skipped for reasons")
        class MyTestCase(unittest.TestCase):

            def setUp(self):
                pytest.pdb_teardown_skipped_class.append("setUp:" + self.id())

            def tearDown(self):
                pytest.pdb_teardown_skipped_class.append("tearDown:" + self.id())

            def test_1(self):
                pass
        """
    )

    result = pytester.runpytest_inprocess("--pdb")
    result.stdout.fnmatch_lines("* 1 skipped in *")
    # Neither setUp nor tearDown should have been called for the skipped class.
    assert tracked == []
