import asyncio
from django.http import HttpResponseNotAllowed
from django.test import RequestFactory, SimpleTestCase
from django.views.generic import View


class AsyncPostOnlyView(View):
    """A view that only accepts POST requests and has async methods."""
    
    async def post(self, request):
        return HttpResponse("ok")


class SyncPostOnlyView(View):
    """A view that only accepts POST requests and has sync methods."""
    
    def post(self, request):
        return HttpResponse("ok")


class TestAsyncHttpMethodNotAllowed(SimpleTestCase):
    """Test that async views properly handle non-allowed HTTP methods."""
    
    def setUp(self):
        self.rf = RequestFactory()
    
    def test_async_view_http_method_not_allowed_should_be_awaitable(self):
        """Test that async views can handle method not allowed without await error."""
        view = AsyncPostOnlyView()
        
        # Create a GET request to trigger the method not allowed response
        request = self.rf.get('/')
        
        # This should not raise "object HttpResponseNotAllowed can't be used in 'await' expression"
        response = view.http_method_not_allowed(request)
        
        # The key test: for async views, this should be awaitable
        # If it's not awaitable, then when the async framework tries to await it, it will fail
        # This is the exact bug described in the issue
        try:
            # Try to await the response - this should work for async views
            async def test_await():
                return await response
            
            # This should not raise TypeError: object HttpResponseNotAllowed can't be used in 'await' expression
            result = asyncio.run(test_await())
            # If we get here without exception, check that it's the right type
            self.assertIsInstance(result, HttpResponseNotAllowed)
        except TypeError as e:
            if "can't be used in 'await' expression" in str(e):
                # This is the exact error from the bug report
                self.fail(f"Async view returned non-awaitable response: {e}")
            else:
                raise  # Re-raise if it's a different TypeError
    
    def test_sync_view_http_method_not_allowed_returns_regular_response(self):
        """Test that sync views return regular HttpResponseNotAllowed."""
        view = SyncPostOnlyView()
        
        # Create a GET request to trigger the method not allowed response
        request = self.rf.get('/')
        
        # For sync views, the response should be a regular HttpResponseNotAllowed
        response = view.http_method_not_allowed(request)
        
        # Should be a regular HttpResponseNotAllowed
        self.assertIsInstance(response, HttpResponseNotAllowed)