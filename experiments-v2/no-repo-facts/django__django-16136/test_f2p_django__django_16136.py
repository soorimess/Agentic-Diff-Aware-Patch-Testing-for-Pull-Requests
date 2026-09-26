"""
Regression test for Django issue where HttpResponseNotAllowed can't be used in 'await' expression
when an async view only supports POST method and a GET request is made.
"""
import asyncio
from django.test import TestCase
from django.http import HttpResponse
from django.views.generic import View
from django.test import RequestFactory


class AsyncPostOnlyView(View):
    """A view that only supports POST requests and is async"""
    
    async def post(self, request):
        return HttpResponse("ok")


class TestAsyncViewMethodNotAllowed(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_async_view_http_method_not_allowed_returns_coroutine(self):
        """
        Test that when an async view only supports POST and GET is requested,
        http_method_not_allowed returns a coroutine that can be awaited
        (this is the fix for the TypeError about HttpResponseNotAllowed not being awaitable)
        """
        # Create an instance of the async view
        view_instance = AsyncPostOnlyView()
        
        # Verify it's marked as async
        self.assertTrue(view_instance.view_is_async)
        
        # Create a proper request
        request = self.factory.get('/test/')
        
        # Call the method that was fixed
        response = view_instance.http_method_not_allowed(request, 'arg1', 'arg2')
        
        # The fix ensures that when view_is_async is True, 
        # http_method_not_allowed returns a coroutine that can be awaited
        # This prevents the TypeError: object HttpResponseNotAllowed can't be used in 'await' expression
        if view_instance.view_is_async:
            # In the fixed version, this should be awaitable (a coroutine)
            # In the buggy version, this would be HttpResponseNotAllowed which is not awaitable
            self.assertTrue(asyncio.iscoroutine(response), 
                          "When view_is_async is True, http_method_not_allowed should return a coroutine")
        else:
            # Should be a normal response
            self.assertFalse(asyncio.iscoroutine(response))
            
        # The test passes if we don't get the specific TypeError
        # The key assertion is that the return type is correct
        self.assertIsNotNone(response)
