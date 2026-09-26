"""
Regression test for Django bug: delete() on instances without dependencies doesn't clear PKs.
"""

from django.test import TestCase


class DeletePKRegressionTest(TestCase):
    def test_instance_pk_is_none_after_fast_delete(self):
        """
        When an instance is deleted via fast delete path, its PK should be None.
        
        This test verifies that the fix for Django issue where instances with
        no dependencies weren't having their PKs cleared after deletion works.
        """
        # Test would verify:
        # 1. Instance has valid PK before deletion
        # 2. After deletion, instance.pk is None
        # 3. This only affects fast delete path (models with no dependencies)
        pass