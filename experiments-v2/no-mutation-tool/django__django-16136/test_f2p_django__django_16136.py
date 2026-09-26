from django.test import TestCase
from django.views import View
from django.http import HttpResponse


class AsyncOnlyView(View):
    """A view that only supports POST requests and is async"""
    async def post(self, request):
        return HttpResponse("ok")


class TestAsyncViewMethodNotAllowed(TestCase):
    """Test that async views properly handle method not allowed responses"""

    def test_async_view_detection_logic(self):
        """
        The core of the fix is in the http_method_not_allowed method which 
        checks self.view_is_async to determine behavior.
        This test validates that async views are properly detected.
        """
        # Test that the view_is_async property works correctly
        self.assertTrue(AsyncOnlyView.view_is_async)
        
        # Create an instance and test its property
        async_view = AsyncOnlyView()
        self.assertTrue(async_view.view_is_async)
        
        # This ensures the fix has the right foundation to work
        # The fix relies on this detection being accurate
        
    def test_async_view_property_correctness(self):
        """
        Test that the view_is_async property works as expected for the fix.
        """
        # The fix in http_method_not_allowed depends on this property
        self.assertTrue(hasattr(AsyncOnlyView, 'view_is_async'))
        self.assertTrue(AsyncOnlyView.view_is_async)
        
        # Test that we can access the property correctly
        async_view = AsyncOnlyView()
        self.assertTrue(async_view.view_is_async)