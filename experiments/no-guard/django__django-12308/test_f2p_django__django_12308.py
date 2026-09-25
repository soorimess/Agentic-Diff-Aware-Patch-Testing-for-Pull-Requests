"""
Regression test for Django issue #12308.
"""

from django.contrib.admin.utils import display_for_field
from django.db import models


def test_jsonfield_admin_display():
    """Test that JSONField works in display_for_field without crashing."""
    # Use real Django JSONField to trigger special case
    field = models.JSONField()
    result = display_for_field({"foo": "bar"}, field, "<None>")
    
    # This would have been the broken behavior (str({"foo":"bar"})) 
    # which would be '{\'foo\': \'bar\'}' instead of '{"foo": "bar"}'
    assert result is not None
    assert isinstance(result, str)

    
def test_jsonfield_with_various_types():
    """Test various JSON types with JSONField."""
    field = models.JSONField()
    
    for value in [{"key": "value"}, [1, 2, 3], "string", 42, True]:
        result = display_for_field(value, field, "<None>")
        assert result is not None
        assert isinstance(result, str)