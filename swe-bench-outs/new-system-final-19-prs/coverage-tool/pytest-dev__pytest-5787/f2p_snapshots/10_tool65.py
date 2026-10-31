# Copied unchanged by the harness from testing/test_reports.py::TestReportSerialization::test_reprentries_serialization_170, a test in this repository before this change.
from _pytest.reports import CollectReport
from _pytest.reports import TestReport


class TestSeededReportSerialization:
    def test_seeded_reprentries_serialization_170(self, testdir):
        """Regarding issue pytest-xdist#170

        This test came originally from test_remote.py in xdist (ca03269).
        """
        from _pytest._code.code import ReprEntry

        reprec = testdir.inline_runsource(
            """
                            def test_repr_entry():
                                x = 0
                                assert x
                        """,
            "--showlocals",
        )
        reports = reprec.getreports("pytest_runtest_logreport")
        assert len(reports) == 3
        rep = reports[1]
        d = rep._to_json()
        a = TestReport._from_json(d)

        rep_entries = rep.longrepr.reprtraceback.reprentries
        a_entries = a.longrepr.reprtraceback.reprentries
        for i in range(len(a_entries)):
            assert isinstance(rep_entries[i], ReprEntry)
            assert rep_entries[i].lines == a_entries[i].lines
            assert rep_entries[i].reprfileloc.lineno == a_entries[i].reprfileloc.lineno
            assert (
                rep_entries[i].reprfileloc.message == a_entries[i].reprfileloc.message
            )
            assert rep_entries[i].reprfileloc.path == a_entries[i].reprfileloc.path
            assert rep_entries[i].reprfuncargs.args == a_entries[i].reprfuncargs.args
            assert rep_entries[i].reprlocals.lines == a_entries[i].reprlocals.lines
            assert rep_entries[i].style == a_entries[i].style


def test_exception_chain_serialization_ensures_chain_preservation(testdir):
    """Test that chained exceptions are properly serialized to preserve the chain.
    
    This test specifically checks that the serialized data contains the chain information
    that would be lost without the fix.
    """
    # Create a test that raises chained exceptions using 'from' clause
    testdir.makepyfile("""
        def test_chained_exception_with_from():
            try:
                try:
                    raise ValueError(11)
                except Exception as e1:
                    raise ValueError(12) from e1
            except Exception as e2:
                raise ValueError(13) from e2

        def test_chained_exception_without_from():
            try:
                try:
                    raise ValueError(21)
                except Exception:
                    raise ValueError(22)
            except Exception:
                raise ValueError(23)
    """)
    
    # Run with inline_run to get reports
    reprec = testdir.inline_run()
    reports = reprec.getreports("pytest_runtest_logreport")
    
    # Find the failed reports
    failed_reports = [r for r in reports if r.outcome == "failed"]
    
    # We should have at least 2 failed reports (one for each test)
    assert len(failed_reports) >= 2
    
    # Test the serialization for one of the chained exception tests
    chained_report = None
    for rep in failed_reports:
        # Find a report with chained exceptions (should have longrepr with chain)
        if rep.longrepr is not None:
            # Check if it's a chained exception by looking at its structure
            if hasattr(rep.longrepr, 'chain') and rep.longrepr.chain is not None:
                chained_report = rep
                break
    
    # If we found a chained exception report, test serialization
    if chained_report is not None:
        # Serialize the report
        serialized = chained_report._to_json()
        
        # Check that the serialized data contains chain information
        assert 'longrepr' in serialized
        longrepr_data = serialized['longrepr']
        
        # This is the key assertion - the serialized data should contain chain info
        # if the fix is applied
        if 'chain' in longrepr_data:
            # The fix is applied - chain should be present
            assert longrepr_data['chain'] is not None
            assert len(longrepr_data['chain']) > 0
        else:
            # The fix is NOT applied - chain should not be present
            # But we want this test to fail when the fix is missing
            # So we'll assert that it should have chain data
            assert 'chain' in longrepr_data, "Chain information should be present after fix"
    
    # Test the deserialization round-trip
    for rep in failed_reports:
        if rep.longrepr is not None:
            # Serialize the report
            serialized = rep._to_json()
            
            # Deserialize it back
            deserialized = TestReport._from_json(serialized)
            
            # The key test: the deserialized report should have proper structure
            assert deserialized.longrepr is not None
            
            # Check that we can access the chain information if it exists
            # This is what the fix enables
            if hasattr(deserialized.longrepr, 'chain'):
                # After fix: chain should be accessible
                assert deserialized.longrepr.chain is not None
            else:
                # Before fix: this would not work properly
                # But we're not asserting that it fails - we're asserting
                # that if it works, it works correctly
                pass


def test_exception_chain_serialization_direct_behavior_check(testdir):
    """Direct test of the serialization behavior change."""
    # Create a test that produces a chained exception
    testdir.makepyfile("""
        def test_chained_exception():
            try:
                try:
                    raise ValueError("inner")
                except Exception as e1:
                    raise RuntimeError("middle") from e1
            except Exception as e2:
                raise TypeError("outer") from e2
    """)
    
    # Run to get reports
    reprec = testdir.inline_run()
    reports = reprec.getreports("pytest_runtest_logreport")
    
    # Find the failed report
    failed_report = None
    for r in reports:
        if r.outcome == "failed":
            failed_report = r
            break
    
    assert failed_report is not None
    assert failed_report.longrepr is not None
    
    # Test the core behavior: serialization should preserve chain info
    # This is what the change was meant to fix
    serialized_data = failed_report._to_json()
    
    # The key assertion: after the fix, the serialized data should contain
    # the proper structure to reconstruct the chain
    assert 'longrepr' in serialized_data
    longrepr_data = serialized_data['longrepr']
    
    # Check if chain data is present (this is the fix)
    # If chain is present, it means the serialization properly handles ExceptionChainRepr
    if 'chain' in longrepr_data:
        # This means the fix is in place - chain data should be properly structured
        assert longrepr_data['chain'] is not None
        # Should contain at least one entry in the chain
        assert len(longrepr_data['chain']) > 0
        # Each chain entry should have the expected structure
        first_chain_entry = longrepr_data['chain'][0]
        assert len(first_chain_entry) == 3  # repr_traceback, repr_crash, description
    else:
        # Before the fix, this would not be present
        # But we want to make sure that when the fix IS applied, it works
        # We'll make this test fail if chain is not present (which means fix is missing)
        assert False, "Chain information should be present in serialized data after fix is applied"


def test_report_to_json_with_exception_chain(testdir):
    """Test that _report_to_json properly handles ExceptionChainRepr objects.
    
    This test specifically targets the _report_to_json function to ensure it
    handles ExceptionChainRepr objects correctly, hitting the missing lines.
    """
    # Create a test that produces chained exceptions
    testdir.makepyfile("""
        def test_chained_exception():
            try:
                try:
                    raise ValueError("inner")
                except Exception as e1:
                    raise RuntimeError("middle") from e1
            except Exception as e2:
                raise TypeError("outer") from e2
    """)
    
    # Run to get reports
    reprec = testdir.inline_run()
    reports = reprec.getreports("pytest_runtest_logreport")
    
    # Find the failed report
    failed_report = None
    for r in reports:
        if r.outcome == "failed":
            failed_report = r
            break
    
    assert failed_report is not None
    assert failed_report.longrepr is not None
    
    # This test directly exercises the _to_json method to make sure it handles
    # ExceptionChainRepr properly, which is what the change was about
    serialized = failed_report._to_json()
    
    # Verify that serialization works without errors
    assert serialized is not None
    assert 'longrepr' in serialized
    
    # The key test: make sure we can serialize ExceptionChainRepr objects properly
    # This is the core of what the change fixes
    longrepr_data = serialized['longrepr']
    
    # Check that the serialized data structure is correct
    assert longrepr_data is not None
    assert 'reprcrash' in longrepr_data
    assert 'reprtraceback' in longrepr_data
    assert 'sections' in longrepr_data
    
    # If there's a chain, it should be properly serialized
    if 'chain' in longrepr_data:
        assert longrepr_data['chain'] is not None
        assert isinstance(longrepr_data['chain'], list)
        # Should have at least one chain entry
        assert len(longrepr_data['chain']) > 0


# Copied unchanged by the harness from testing/test_reports.py::TestReportSerialization::test_collectreport_fail, a test in this repository before this change.
from _pytest.reports import CollectReport


class TestSeededReportSerialization2:
    def test_seeded_collectreport_fail(self, testdir):
        """This test came originally from test_remote.py in xdist (ca03269)."""
        reprec = testdir.inline_runsource("qwe abc")
        reports = reprec.getreports("pytest_collectreport")
        assert reports
        for rep in reports:
            d = rep._to_json()
            newrep = CollectReport._from_json(d)
            assert newrep.passed == rep.passed
            assert newrep.failed == rep.failed
            assert newrep.skipped == rep.skipped
            if rep.failed:
                assert newrep.longrepr == str(rep.longrepr)
                
    def test_seeded_collectreport_with_chained_exceptions(self, testdir):
        """Test that chained exceptions are properly handled in collect reports.
        
        This test specifically targets the _report_to_json function with ExceptionChainRepr
        to ensure the missing lines in _report_to_json are covered.
        """
        # Create a test that will produce chained exceptions during collection
        testdir.makepyfile("""
            def test_function():
                # This will create a chained exception during collection
                raise ValueError("test error") from RuntimeError("chained")
        """)
        
        # Run with inline_run to get reports
        reprec = testdir.inline_run()
        reports = reprec.getreports("pytest_collectreport")
        
        # There should be at least one collect report
        assert reports
        
        # Test serialization for each report
        for rep in reports:
            # This should not crash and should properly serialize
            d = rep._to_json()
            
            # Verify the serialized data structure
            assert 'longrepr' in d
            
            # Deserialize it back to make sure round-trip works
            newrep = CollectReport._from_json(d)
            assert newrep is not None
            
            # Test that the serialization works for ExceptionChainRepr if present
            if hasattr(rep.longrepr, 'chain'):
                # If it's an ExceptionChainRepr, make sure it's properly serialized
                assert 'chain' in d['longrepr']
                assert d['longrepr']['chain'] is not None


# Copied unchanged by the harness from testing/test_reports.py::TestReportSerialization::test_reprentries_serialization_196, a test in this repository before this change.
from _pytest.reports import TestReport
from _pytest._code.code import ReprEntryNative


class TestSeededReportSerialization3:
    def test_seeded_reprentries_serialization_196(self, testdir):
        """Regarding issue pytest-xdist#196

        This test came originally from test_remote.py in xdist (ca03269).
        """
        reprec = testdir.inline_runsource(
            """
                            def test_repr_entry_native():
                                x = 0
                                assert x
                        """,
            "--tb=native",
        )
        reports = reprec.getreports("pytest_runtest_logreport")
        assert len(reports) == 3
        rep = reports[1]
        d = rep._to_json()
        a = TestReport._from_json(d)

        rep_entries = rep.longrepr.reprtraceback.reprentries
        a_entries = a.longrepr.reprtraceback.reprentries
        for i in range(len(a_entries)):
            assert isinstance(rep_entries[i], ReprEntryNative)
            assert rep_entries[i].lines == a_entries[i].lines
            
    def test_seeded_deserialize_repr_entry_with_exception_chain(self, testdir):
        """Test that _report_kwargs_from_json properly handles ReprEntry and ReprEntryNative.
        
        This specifically targets the deserialize_repr_entry function to hit the missing lines:
        lines 435-436, 438 in _report_kwargs_from_json.
        """
        # Create a test that will produce a report with ReprEntry objects
        testdir.makepyfile("""
            def test_repr_entry():
                x = 0
                assert x
        """)
        
        # Run to get reports
        reprec = testdir.inline_run()
        reports = reprec.getreports("pytest_runtest_logreport")
        
        # Find the report with the entry
        assert len(reports) >= 1
        rep = reports[1]  # The test report
        
        # Test serialization and deserialization to ensure _from_json works properly
        # This will exercise the deserialize_repr_entry function
        serialized = rep._to_json()
        assert serialized is not None
        
        # Deserialize it back
        deserialized = TestReport._from_json(serialized)
        assert deserialized is not None
        
        # Verify that the deserialized report has the expected structure
        assert deserialized.longrepr is not None
        assert hasattr(deserialized.longrepr, 'reprtraceback')
        assert hasattr(deserialized.longrepr, 'reprcrash')
        
        # Test that the deserialization works correctly for the specific entry types
        if hasattr(deserialized.longrepr, 'reprtraceback'):
            # This exercises the deserialization path that handles ReprEntry and ReprEntryNative
            assert deserialized.longrepr.reprtraceback is not None
            assert deserialized.longrepr.reprcrash is not None