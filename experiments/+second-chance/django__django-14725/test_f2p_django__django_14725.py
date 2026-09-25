from django.test import TestCase


class ModelFormsetEditOnlyTests(TestCase):
    """
    Test that model formsets can disallow new object creation with edit_only=True.
    In the original bug report, model formsets don't provide a way to create an 
    "edit only" view of objects.
    """
    
    def test_modelformset_factory_accepts_edit_only_parameter(self):
        """
        modelformset_factory should accept an edit_only parameter.
        This test validates that the edit_only parameter can be passed without error.
        """
        from django.forms.models import modelformset_factory
        from django.db import models
        
        # Use the external test models that should be available
        from tests.model_formsets.models import Author, Book
        
        # This should not raise an exception
        BookFormSet = modelformset_factory(Book, fields=['title'], edit_only=True)
        
        # The edit_only attribute should be set on the FormSet class
        self.assertTrue(hasattr(BookFormSet, 'edit_only'))
        self.assertTrue(BookFormSet.edit_only)
        
    def test_inlineformset_factory_accepts_edit_only_parameter(self):
        """
        inlineformset_factory should accept an edit_only parameter.
        """
        from django.forms.models import inlineformset_factory
        from django.db import models
        
        # Use the external test models that should be available  
        from tests.model_formsets.models import Author, Book
        
        # This should not raise an exception
        BookInlineFormSet = inlineformset_factory(Author, Book, fields=['title'], edit_only=True)
        
        # The edit_only attribute should be set on the FormSet class
        self.assertTrue(hasattr(BookInlineFormSet, 'edit_only'))
        self.assertTrue(BookInlineFormSet.edit_only)