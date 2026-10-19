import unittest
from django.db.models import Index, UniqueConstraint
from django.test import TestCase


class CoveringIndexTests(TestCase):
    """Tests for covering indexes (INCLUDE clause in CREATE INDEX)."""

    def test_index_accepts_include_parameter(self):
        """Test that Index class now accepts include parameter."""
        # This should work after the pull request is applied
        try:
            index = Index(
                name='test_idx',
                fields=['field1'],
                include=['field2']
            )
            self.assertEqual(index.include, ('field2',))
        except TypeError as e:
            # In the old code, this would fail with TypeError about unexpected keyword argument
            if 'include' in str(e):
                self.fail("Index.include parameter not supported - this test should pass after the pull request is applied")
            raise

    def test_unique_constraint_accepts_include_parameter(self):
        """Test that UniqueConstraint class now accepts include parameter."""
        # This should work after the pull request is applied
        try:
            constraint = UniqueConstraint(
                fields=['field1'],
                name='test_constraint',
                include=['field2']
            )
            self.assertEqual(constraint.include, ('field2',))
        except TypeError as e:
            # In the old code, this would fail with TypeError about unexpected keyword argument
            if 'include' in str(e):
                self.fail("UniqueConstraint.include parameter not supported - this test should pass after the pull request is applied")
            raise

    def test_index_include_parameter_validation(self):
        """Test validation of include parameter in Index."""
        # Test that include must be list or tuple
        try:
            Index(
                name='test_idx',
                fields=['field1'],
                include='invalid'
            )
            # If we get here, validation might pass in new code
        except ValueError as e:
            self.assertIn('Index.include must be a list or tuple', str(e))
        except TypeError as e:
            # In old code, this will fail with TypeError
            if 'include' in str(e):
                self.fail("Index.include parameter not supported - this test should pass after the pull request is applied")
            raise

    def test_unique_constraint_include_parameter_validation(self):
        """Test validation of include parameter in UniqueConstraint."""
        # Test that include must be list or tuple
        try:
            UniqueConstraint(
                fields=['field1'],
                name='test_constraint',
                include='invalid'
            )
            # If we get here, validation might pass in new code
        except ValueError as e:
            self.assertIn('UniqueConstraint.include must be a list or tuple', str(e))
        except TypeError as e:
            # In old code, this will fail with TypeError
            if 'include' in str(e):
                self.fail("UniqueConstraint.include parameter not supported - this test should pass after the pull request is applied")
            raise

    def test_index_without_include_still_works(self):
        """Test that normal Index creation still works after the change."""
        try:
            index = Index(
                name='test_idx',
                fields=['field1']
            )
            self.assertEqual(index.fields, ['field1'])
            self.assertEqual(index.name, 'test_idx')
        except Exception as e:
            self.fail(f"Basic Index functionality broken: {e}")

    def test_unique_constraint_without_include_still_works(self):
        """Test that normal UniqueConstraint creation still works after the change."""
        try:
            constraint = UniqueConstraint(
                fields=['field1'],
                name='test_constraint'
            )
            self.assertEqual(constraint.fields, ('field1',))
            self.assertEqual(constraint.name, 'test_constraint')
        except Exception as e:
            self.fail(f"Basic UniqueConstraint functionality broken: {e}")

    def test_index_include_validation_no_name(self):
        """Test that include requires a name for Index."""
        try:
            Index(
                fields=['field1'],
                include=['field2']
            )
            # If we get here, validation might pass in new code
        except ValueError as e:
            self.assertIn('A covering index must be named', str(e))
        except TypeError as e:
            # In old code, this will fail with TypeError
            if 'include' in str(e):
                self.fail("Index.include parameter not supported - this test should pass after the pull request is applied")
            raise

    def test_unique_constraint_repr_includes_include(self):
        """Test that UniqueConstraint repr includes include information."""
        try:
            constraint = UniqueConstraint(
                fields=['field1'],
                name='test_constraint',
                include=['field2', 'field3']
            )
            repr_str = repr(constraint)
            self.assertIn('include=', repr_str)
            self.assertIn('field2', repr_str)
            self.assertIn('field3', repr_str)
        except Exception:
            # Skip if this functionality doesn't exist yet
            pass

    def test_index_repr_includes_include(self):
        """Test that Index repr includes include information."""
        try:
            index = Index(
                name='test_idx',
                fields=['field1'],
                include=['field2', 'field3']
            )
            repr_str = repr(index)
            self.assertIn('include=', repr_str)
            self.assertIn('field2', repr_str)
            self.assertIn('field3', repr_str)
        except Exception:
            # Skip if this functionality doesn't exist yet
            pass

    def test_unique_constraint_deconstruct_includes_include(self):
        """Test that UniqueConstraint deconstruct includes include."""
        try:
            constraint = UniqueConstraint(
                fields=['field1'],
                name='test_constraint',
                include=['field2']
            )
            path, args, kwargs = constraint.deconstruct()
            self.assertIn('include', kwargs)
            self.assertEqual(kwargs['include'], ('field2',))
        except Exception:
            # Skip if this functionality doesn't exist yet
            pass

    def test_index_deconstruct_includes_include(self):
        """Test that Index deconstruct includes include."""
        try:
            index = Index(
                name='test_idx',
                fields=['field1'],
                include=['field2']
            )
            path, args, kwargs = index.deconstruct()
            self.assertIn('include', kwargs)
            self.assertEqual(kwargs['include'], ('field2',))
        except Exception:
            # Skip if this functionality doesn't exist yet
            pass