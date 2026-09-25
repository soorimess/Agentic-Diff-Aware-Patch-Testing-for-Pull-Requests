"""
Regression test for Django async View http_method_not_allowed bug.
"""

import asyncio
from django.http import HttpResponseNotAllowed
from django.test import TestCase
from django.views import View
from django.test import RequestFactory


class AsyncPostOnlyView(View):
    """A view that only supports POST requests (asynchronous)."""
    
    async def post(self, request):
        return HttpResponse("ok")


class TestAsyncViewMethodNotAllowed(TestCase):
    """
    Ensure http_method_not_allowed returns an awaitable function for async views.
    This is needed to prevent:
    TypeError: object HttpResponseNotAllowed can't be used in 'await' expression
    """
    
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_async_view_method_not_allowed_returns_awaitable(self):
        """
        Test that for async views, http_method_not_allowed returns a coroutine function.
        This prevents TypeError when Django's async handler awaits the response.
        """
        # Create async view instance
        async_view = AsyncPostOnlyView()
        self.assertTrue(async_view.view_is_async)
        
        # Call http_method_not_allowed
        request = self.factory.get('/test/')
        response = async_view.http_method_not_allowed(request)
        
        # The fix: this should return an awaitable function
        # This test should FAIL in the ORIGINAL buggy version 
        # and PASS in the FIXED version
        self.assertTrue(
            asyncio.iscoroutinefunction(response),
            "For async views, http_method_not_allowed must return an awaitable coroutine function"
        )