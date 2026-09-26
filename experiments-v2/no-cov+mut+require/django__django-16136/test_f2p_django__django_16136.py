import asyncio
from django.http import HttpResponse, HttpResponseNotAllowed
from django.test import TestCase, RequestFactory
from django.views import View


class AsyncPostOnlyView(View):
    """A view that only supports POST requests and is async."""
    async def post(self, request):
        return HttpResponse("ok")


class TestAsyncViewMethodNotAllowed(TestCase):
    def setUp(self):
        self.rf = RequestFactory()
    
    def test_async_view_http_method_not_allowed_returns_coroutine_function(self):
        """
        Test that when an async view with only POST method receives a GET request,
        http_method_not_allowed returns a coroutine function that can be awaited.
        """
        # Create an instance of the async view
        view = AsyncPostOnlyView()
        
        # Check that the view is detected as async
        self.assertTrue(view.view_is_async)
        
        # Create a GET request
        request = self.rf.get('/test/')
        
        # Call http_method_not_allowed - this is what gets called when a GET
        # request is made to an async view that only supports POST
        response = view.http_method_not_allowed(request)
        
        # The fix ensures that when view_is_async is True, we return a coroutine function
        # that can be awaited, not a regular HttpResponse
        # Before the fix: response was HttpResponseNotAllowed (not awaitable)
        # After the fix: response is a coroutine function (awaitable)
        
        # This is the core test - we want to make sure we get a coroutine function
        # when the view is async, which means it can be awaited
        self.assertTrue(
            asyncio.iscoroutinefunction(response),
            "When view_is_async is True, http_method_not_allowed should return a coroutine function"
        )