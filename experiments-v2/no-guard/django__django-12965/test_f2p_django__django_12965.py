from django.db import connection
from django.test import TestCase

from django.db.models.sql.compiler import SQLDeleteCompiler
from django.db.models.sql.query import Query


class DeleteSQLGenerationTest(TestCase):
    def test_single_alias_property_does_not_crash(self):
        """
        Regression test for Django ticket #12965.
        
        The fix in SQLDeleteCompiler.single_alias ensures that get_initial_alias() 
        is called to prevent crashes when accessing alias_refcount on minimal queries.
        This prevents the crash that would occur in the old buggy implementation.
        """
        # Create a minimal query that would cause crashes in the old code
        query = Query(model=None)
        
        # Create compiler - this should not crash with the fix
        compiler = SQLDeleteCompiler(query, connection, 'default')
        
        # The fix prevents crashes by ensuring get_initial_alias() is called
        # This should work without raising an exception
        try:
            result = compiler.single_alias
            # Should return a boolean value
            self.assertIsInstance(result, bool)
        except AttributeError as e:
            if "'NoneType' object has no attribute '_meta'" in str(e):
                # This is the specific crash that the fix prevents
                # If we get this error, it means the fix is not working
                self.fail("single_alias property crashes - fix not applied correctly")
            else:
                raise  # Re-raise different AttributeError
        except Exception as e:
            # Any other exception is unexpected
            self.fail(f"Unexpected exception in single_alias: {e}")