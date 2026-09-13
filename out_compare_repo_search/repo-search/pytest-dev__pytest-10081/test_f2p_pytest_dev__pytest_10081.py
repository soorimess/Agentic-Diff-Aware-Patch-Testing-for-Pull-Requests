def test_unittest_class_skip_does_not_run_tearDown_with_pdb(pytester):
    import _pytest

    class _DummyPdb:
        quitting = False

        def __init__(self, *args, **kwargs):
            pass

        def reset(self):
            pass

        def interaction(self, *args, **kwargs):
            pass

    _pytest._CustomPdb = _DummyPdb  # type: ignore[attr-defined]
    try:
        p = pytester.makepyfile(
            """
            import unittest

            @unittest.skip("skip class")
            class MyTestCase(unittest.TestCase):
                def setUp(self):
                    raise RuntimeError("setUp should not be called")

                def test_one(self):
                    pass

                def tearDown(self):
                    # should not be executed for a skipped class; cause NameError if it runs
                    undefined_name
            """
        )
        # pass --pdb and custom pdb class to avoid interactive prompt
        result = pytester.runpytest_inprocess("--pdb", "--pdbcls=_pytest:_CustomPdb", p)
        # ensure the run reported a skipped test and did not execute tearDown (no NameError)
        result.stdout.fnmatch_lines(["*1 skipped*"])
        assert not any("NameError" in line or "undefined_name" in line for line in result.stdout.lines)
    finally:
        try:
            delattr(_pytest, "_CustomPdb")
        except Exception:
            pass
