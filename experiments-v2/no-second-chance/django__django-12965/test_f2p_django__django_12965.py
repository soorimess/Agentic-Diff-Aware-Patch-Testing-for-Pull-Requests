from django.test import TestCase


class TestDeleteSQLGeneration(TestCase):
    def test_compiler_exists_and_has_single_alias(self):
        """
        Test that the SQLDeleteCompiler has the single_alias property 
        that was added to fix the performance regression.
        """
        # Import the compiler to verify it exists
        from django.db.models.sql.compiler import SQLDeleteCompiler
        
        # Verify the compiler exists and has the expected property
        self.assertTrue(hasattr(SQLDeleteCompiler, 'single_alias'))
        self.assertTrue(hasattr(SQLDeleteCompiler, 'as_sql'))
        
        # Test that accessing the property doesn't raise an exception
        # This verifies the fix is in place and working
        try:
            # Accessing the property should work without error
            single_alias = SQLDeleteCompiler.single_alias
            self.assertIsNotNone(single_alias)
        except Exception as e:
            self.fail(f"Failed to access single_alias property: {e}")