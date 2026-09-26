import asyncio
from unittest.mock import Mock

from django.http import HttpResponseNotAllowed
from django.test import TestCase
from django.views import View


class AsyncPostOnlyView(View):
    """A view that only supports POST requests (async)"""
    async def post(self, request):
        return HttpResponse("ok")


class TestAsyncViewMethodNotAllowed(TestCase):
    def test_async_view_http_method_not_allowed_prevents_typeerror(self):
        """
        Test that async views don't cause TypeError when http_method_not_allowed is called
        with a disallowed method.
        
        This test directly tests the bug: "object HttpResponseNotAllowed can't be used in 'await' expression"
        """
        # Create an async view instance
        instance = AsyncPostOnlyView()
        
        # Verify this is an async view
        self.assertTrue(instance.__class__.view_is_async)
        
        # Create a mock request object to pass to http_method_not_allowed
        mock_request = Mock()
        mock_request.method = "GET"
        mock_request.path = "/test/"
        mock_request.META = {}
        
        # Call http_method_not_allowed directly
        response = instance.http_method_not_allowed(mock_request)
        
        # The bug occurs when trying to await response in async context
        # Before the fix: response is HttpResponseNotAllowed (not awaitable)
        # After the fix: response is awaitable function
        
        # Test that we can actually await the response without getting TypeError
        # This is what the fix prevents
        try:
            # Try to await the response - this should not raise TypeError
            async def test_await():
                return await response
            
            loop = asyncio.new_event_loop()
            try:
                # This should work after the fix
                result = loop.run_until_complete(test_await())
                # If we get here, it means the response was awaitable
                # Verify it's the right type of response
                self.assertIsInstance(result, HttpResponseNotAllowed)
            finally:
                loop.close()
                
        except TypeError as e:
            if "can't be used in 'await' expression" in str(e):
                # This is the bug we're trying to prevent
                self.fail("TypeError occurred: %s - this indicates the bug exists" % str(e))
            else:
                raise  # Some other TypeError, re-raise

    def test_sync_view_returns_regular_response(self):
        """Test that sync views return regular responses from http_method_not_allowed"""
        # Create a sync view instance (by default, View is sync)
        from django.views.generic.base import View
        
        # Test that the default view is not async
        self.assertFalse(View.view_is_async)
        
        # Create a mock request object to pass to http_method_not_allowed
        mock_request = Mock()
        mock_request.method = "GET"
        mock_request.path = "/test/"
        mock_request.META = {}
        
        # Call http_method_not_allowed directly on the base View class
        response = View().http_method_not_allowed(mock_request)
        
        # For sync views, the response should be a regular HttpResponseNotAllowed
        self.assertIsInstance(response, HttpResponseNotAllowed)