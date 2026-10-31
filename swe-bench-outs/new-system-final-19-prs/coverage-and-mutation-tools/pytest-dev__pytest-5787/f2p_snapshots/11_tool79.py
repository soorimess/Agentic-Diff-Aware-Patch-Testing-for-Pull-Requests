import pytest
from _pytest.reports import TestReport
from _pytest._code.code import ExceptionChainRepr, ReprTraceback, ReprFileLocation, ReprEntry, ReprEntryNative, ReprFuncArgs, ReprLocals
from _pytest.reports import CollectReport


def test_exception_chain_serialization_preserves_chain_info():
    """Test that ExceptionChainRepr objects are properly serialized with chain information."""
    
    # Create a mock ExceptionChainRepr with chain data
    reprtraceback1 = ReprTraceback([], "some extraline", "long")
    reprcrash1 = ReprFileLocation("file.py", 10, "line1")
    
    reprtraceback2 = ReprTraceback([], "some extraline", "long")
    reprcrash2 = ReprFileLocation("file.py", 15, "line2")
    
    # Create the chain data as it would be in an ExceptionChainRepr
    chain = [
        (reprtraceback1, reprcrash1, "The above exception was the direct cause of the following exception:"),
        (reprtraceback2, reprcrash2, None),  # Last exception in chain
    ]
    
    exception_chain_repr = ExceptionChainRepr(chain)
    
    # Create a TestReport with this ExceptionChainRepr
    report = TestReport(
        nodeid="test_node",
        location=("test_file.py", 1, "test_func"),
        keywords={},
        outcome="failed",
        longrepr=exception_chain_repr,
        when="call",
        sections=[],
    )
    
    # Serialize the report
    serialized = report._to_json()
    
    # Check that the serialized data contains chain information
    assert "longrepr" in serialized
    assert "chain" in serialized["longrepr"]
    assert serialized["longrepr"]["chain"] is not None
    assert len(serialized["longrepr"]["chain"]) == 2
    
    # Deserialize the report
    deserialized = TestReport._from_json(serialized)
    
    # Verify that chain information is preserved
    assert hasattr(deserialized.longrepr, 'chain')
    assert deserialized.longrepr.chain is not None
    assert len(deserialized.longrepr.chain) == 2


def test_exception_chain_serialization_with_none_chain():
    """Test that reports without chain data serialize correctly."""
    
    # Create a regular ReprExceptionInfo (not ExceptionChainRepr)
    reprtraceback = ReprTraceback([], "some extraline", "long")
    reprcrash = ReprFileLocation("file.py", 10, "line1")
    
    from _pytest._code.code import ReprExceptionInfo
    exception_info = ReprExceptionInfo(reprtraceback, reprcrash)
    
    # Create a TestReport with this
    report = TestReport(
        nodeid="test_node",
        location=("test_file.py", 1, "test_func"),
        keywords={},
        outcome="failed",
        longrepr=exception_info,
        when="call",
        sections=[],
    )
    
    # Serialize the report
    serialized = report._to_json()
    
    # Check that the serialized data does not have chain information for non-chain cases
    assert "longrepr" in serialized
    assert "chain" in serialized["longrepr"]
    assert serialized["longrepr"]["chain"] is None
    
    # Deserialize the report
    deserialized = TestReport._from_json(serialized)
    
    # Verify that it's still a ReprExceptionInfo (not ExceptionChainRepr)
    from _pytest._code.code import ReprExceptionInfo
    assert isinstance(deserialized.longrepr, ReprExceptionInfo)
    assert not hasattr(deserialized.longrepr, 'chain')


def test_exception_chain_serialization_preserves_chain_elements():
    """Test that individual chain elements are properly serialized."""
    
    # Create a more complex chain
    reprtraceback1 = ReprTraceback([], "extraline1", "long")
    reprcrash1 = ReprFileLocation("file1.py", 5, "line1")
    
    reprtraceback2 = ReprTraceback([], "extraline2", "short")
    reprcrash2 = ReprFileLocation("file2.py", 10, "line2")
    
    chain = [
        (reprtraceback1, reprcrash1, "First exception description"),
        (reprtraceback2, reprcrash2, "Second exception description"),
    ]
    
    exception_chain_repr = ExceptionChainRepr(chain)
    
    # Create a TestReport
    report = TestReport(
        nodeid="test_node",
        location=("test_file.py", 1, "test_func"),
        keywords={},
        outcome="failed",
        longrepr=exception_chain_repr,
        when="call",
        sections=[],
    )
    
    # Serialize and deserialize
    serialized = report._to_json()
    deserialized = TestReport._from_json(serialized)
    
    # Verify that chain elements are preserved
    assert deserialized.longrepr.chain is not None
    assert len(deserialized.longrepr.chain) == 2
    
    # Check first element
    first_element = deserialized.longrepr.chain[0]
    assert first_element[0] is not None  # reprtraceback
    assert first_element[1] is not None  # reprcrash
    assert first_element[2] == "First exception description"
    
    # Check second element
    second_element = deserialized.longrepr.chain[1]
    assert second_element[0] is not None  # reprtraceback
    assert second_element[1] is not None  # reprcrash
    assert second_element[2] == "Second exception description"


def test_report_with_repr_entries_serializes_properly():
    """Test that TestReport with ReprEntry objects exercises _report_to_json functions."""
    # Create ReprEntry objects to test serialization
    reprfileloc = ReprFileLocation("test.py", 10, "test line")
    reprfuncargs = ReprFuncArgs([("arg1", "value1")])
    reprlocals = ReprLocals(["local_var = 'value'"])
    
    repr_entry = ReprEntry(
        lines=["line1", "line2"],
        reprfuncargs=reprfuncargs,
        reprlocals=reprlocals,
        filelocrepr=reprfileloc,
        style="long"
    )
    
    # Create a TestReport with ReprEntry in traceback to exercise _report_to_json.serialize_repr_entry
    reprtraceback = ReprTraceback([repr_entry], "extraline", "long")
    reprcrash = ReprFileLocation("file.py", 10, "line1")
    from _pytest._code.code import ReprExceptionInfo
    exception_info = ReprExceptionInfo(reprtraceback, reprcrash)
    
    report = TestReport(
        nodeid="test_node",
        location=("test_file.py", 1, "test_func"),
        keywords={},
        outcome="failed",
        longrepr=exception_info,
        when="call",
        sections=[],
    )
    
    # This should exercise the _report_to_json.serialize_repr_entry function
    serialized = report._to_json()
    
    # Verify that the serialization works properly and includes the ReprEntry data
    assert "longrepr" in serialized
    assert "reprtraceback" in serialized["longrepr"]
    assert "reprentries" in serialized["longrepr"]["reprtraceback"]
    assert len(serialized["longrepr"]["reprtraceback"]["reprentries"]) == 1
    
    # Verify the entry type and structure
    entry_data = serialized["longrepr"]["reprtraceback"]["reprentries"][0]
    assert entry_data["type"] == "ReprEntry"
    assert "data" in entry_data
    assert "lines" in entry_data["data"]
    assert "reprfileloc" in entry_data["data"]
    assert "reprfuncargs" in entry_data["data"]
    assert "reprlocals" in entry_data["data"]
    assert "style" in entry_data["data"]


def test_report_with_repr_entry_native_serializes_properly():
    """Test that TestReport with ReprEntryNative objects exercises _report_to_json functions."""
    # Create ReprEntryNative objects to test serialization
    repr_entry_native = ReprEntryNative(["line1", "line2"])
    
    # Create a TestReport with ReprEntryNative in traceback
    reprtraceback = ReprTraceback([repr_entry_native], "extraline", "long")
    reprcrash = ReprFileLocation("file.py", 10, "line1")
    from _pytest._code.code import ReprExceptionInfo
    exception_info = ReprExceptionInfo(reprtraceback, reprcrash)
    
    report = TestReport(
        nodeid="test_node",
        location=("test_file.py", 1, "test_func"),
        keywords={},
        outcome="failed",
        longrepr=exception_info,
        when="call",
        sections=[],
    )
    
    # This should exercise the _report_to_json.serialize_repr_entry function
    serialized = report._to_json()
    
    # Verify that the serialization works properly and includes the ReprEntryNative data
    assert "longrepr" in serialized
    assert "reprtraceback" in serialized["longrepr"]
    assert "reprentries" in serialized["longrepr"]["reprtraceback"]
    assert len(serialized["longrepr"]["reprtraceback"]["reprentries"]) == 1
    
    # Verify the entry type and structure
    entry_data = serialized["longrepr"]["reprtraceback"]["reprentries"][0]
    assert entry_data["type"] == "ReprEntryNative"
    assert "data" in entry_data
    assert "lines" in entry_data["data"]


# Copied unchanged by the harness from testing/test_reports.py::TestReportSerialization::test_reprentries_serialization_170, a test in this repository before this change.
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


# Copied unchanged by the harness from testing/test_reports.py::TestReportSerialization::test_collectreport_fail, a test in this repository before this change.
from _pytest.reports import CollectReport


class TestSeededReportSerialization2:
    def test_seeded_collectreport_fail(self, testdir):
        """This test came originally from test_remote.py in xdist (ca03269)."""
        reprec = testdir.inline_runsource(
            """
            def test_simple():
                assert False
            """
        )
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
                
    def test_seeded_deserialize_repr_entry_native(self, testdir):
        """Test that exercises _report_kwargs_from_json.deserialize_repr_entry for ReprEntryNative."""
        from _pytest._code.code import ReprEntryNative
        
        # Create a test that will generate ReprEntryNative objects
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
        
        # Serialize and deserialize to exercise _report_kwargs_from_json
        d = rep._to_json()
        a = TestReport._from_json(d)
        
        # Verify the deserialization worked correctly
        assert a.nodeid == rep.nodeid
        assert a.outcome == rep.outcome
        assert a.when == rep.when
        
    def test_seeded_from_json_exercises_remaining_lines(self, testdir):
        """Test that exercises the remaining _report_kwargs_from_json line."""
        # This test specifically exercises the _from_json method to cover the last line
        reprec = testdir.inline_runsource(
            """
            def test_simple():
                assert False, "Test message"
            """
        )
        reports = reprec.getreports("pytest_runtest_logreport")
        assert len(reports) >= 1
        
        # Get a report and serialize it
        rep = reports[1]  # Get the test failure report
        d = rep._to_json()
        
        # This call exercises _report_kwargs_from_json (the last remaining line)
        a = TestReport._from_json(d)
        
        # Verify that deserialization works correctly
        assert a.nodeid == rep.nodeid
        assert a.outcome == rep.outcome
        assert a.when == rep.when
        assert a.longrepr is not None