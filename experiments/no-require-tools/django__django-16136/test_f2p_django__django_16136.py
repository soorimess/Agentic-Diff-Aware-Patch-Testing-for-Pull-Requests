"""
Regression test for Django issue where HttpResponseNotAllowed can't be used in 'await' expression.
This occurs when a View subclass with only async methods is called with a method that's not allowed.
"""
from django.http import HttpResponse
from django.test import SimpleTestCase
from django.views import View
from django.http import HttpResponseNotAllowed
import asyncio


class AsyncPostOnlyView(View):
    """A view that only supports POST requests (async)"""
    async def post(self, request):
        return HttpResponse("ok")


class SyncPostOnlyView(View):
    """A view that only supports POST requests (sync)"""
    def post(self, request):
        return HttpResponse("ok")


class HttpResponseNotAllowedAwaitsTest(SimpleTestCase):
    
    def test_async_view_http_method_not_allowed_returns_awaitable(self):
        """
        Test that when an async view's http_method_not_allowed is called,
        it returns something that can be awaited properly.
        
        This is a regression test for the fix that ensures:
        - For async views, http_method_not_allowed returns an awaitable coroutine
        - This prevents the TypeError: object HttpResponseNotAllowed can't be used in 'await' expression
        """
        # Create an async view instance
        view_instance = AsyncPostOnlyView()
        
        # Test the http_method_not_allowed method directly (simulating what Django does)
        from django.http import HttpRequest
        request = HttpRequest()
        request.method = 'GET'
        request.path = '/test/'
        
        # For async views, this should return an awaitable (coroutine function) 
        # that when awaited, returns HttpResponseNotAllowed
        response = view_instance.http_method_not_allowed(request)
        
        # The fix: when view_is_async=True, it should return a coroutine that can be awaited
        # This makes it compatible with Django's async sync bridge
        self.assertTrue(asyncio.iscoroutinefunction(response))
        
        # Verify the correlation: when awaited, should get HttpResponseNotAllowed
        async def check_response():
            awaited_response = await response()
            return awaited_response
        
        result = asyncio.run(check_response())
        self.assertIsInstance(result, HttpResponseNotAllowed)
        
    def test_sync_view_http_method_not_allowed_returns_direct_response(self):
        """
        Test that when a sync view's http_method_not_allowed is called,
        it returns HttpResponseNotAllowed directly (no need for async wrap).
        """
        # Create a sync view instance  
        view_instance = SyncPostOnlyView()
        
        # Test the http_method_not_allowed method directly
        from django.http import HttpRequest
        request = HttpRequest()
        request.method = 'GET'
        request.path = '/test/'
        
        # For sync views, this should return HttpResponseNotAllowed directly
        response = view_instance.http_method_not_allowed(request)
        
        # Should be a direct HttpResponseNotAllowed
        self.assertIsInstance(response, HttpResponseNotAllowed)
        
        # Should not be awaitable/coroutine function
        self.assertFalse(asyncio.iscoroutinefunction(response))