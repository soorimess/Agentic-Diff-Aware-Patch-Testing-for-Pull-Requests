"""
Regression test for Django #13794: add filter is unable to concatenate strings with lazy string
"""

def test_add_filter_with_lazy_strings():
    """Test that add filter concatenates strings properly with lazy strings."""
    from django.template import Template, Context
    from django.utils.functional import lazy
    
    def lazy_string():
        return "world"
    
    # Create lazy string 
    lazy_world = lazy(lazy_string, str)()
    
    # Test template with add filter
    template = Template("{{ value|add:lazy_value }}")
    context = Context({
        'value': 'hello ',
        'lazy_value': lazy_world
    })
    
    result = template.render(context)
    
    # This should work correctly after fix, returning "hello world" 
    # instead of empty string or TypeError
    assert result == 'hello world'