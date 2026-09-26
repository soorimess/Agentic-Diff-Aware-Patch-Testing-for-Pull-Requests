import asyncio
from django.http import HttpResponse, HttpResponseNotAllowed
from django.test import SimpleTestCase
from django.views import View


class AsyncPostOnlyView(View):
    """A view that only supports POST requests and is async."""
    
    async def post(self, request):
        return HttpResponse("ok")


class TestAsyncViewMethodNotAllowed(SimpleTestCase):
    """Test that async views properly handle method not allowed responses."""
    
    def test_async_view_returns_awaitable_method_not_allowed_response(self):
        """
        Test that when an async view only supports POST but GET is requested,
        the http_method_not_allowed method returns a response that can be awaited.
        """
        # Create an instance of our async view
        view = AsyncPostOnlyView()
        
        # Check that the view is correctly identified as async
        self.assertTrue(view.__class__.view_is_async)
        
        # Create a mock request object
        from django.http import HttpRequest
        request = HttpRequest()
        request.method = 'GET'
        request.path = '/test/'
        
        # Call the http_method_not_allowed method directly
        response = view.http_method_not_allowed(request)
        
        # For async views, the response should be awaitable
        # This is the core issue: currently it returns HttpResponseNotAllowed directly
        # but should return a coroutine function that wraps it
        if view.__class__.view_is_async:
            # This should pass once the fix is applied
            # Currently it fails because response is not callable
            self.assertTrue(
                callable(response), 
                "For async views, http_method_not_allowed should return a callable (coroutine function)"
            )
            
            # Test that we can actually await it
            async def test_await():
                return await response()
            
            # This should work without TypeError about HttpResponseNotAllowed not being awaitable
            try:
                result = asyncio.run(test_await())
                self.assertEqual(result.status_code, 405)
            except TypeError as e:
                if "object HttpResponseNotAllowed can't be used in 'await' expression" in str(e):
                    self.fail("Async view's http_method_not_allowed returned non-awaitable response")
                else:
                    raise
        else:
            # For sync views, it should return HttpResponse directly
            self.assertIsInstance(response, HttpResponseNotAllowed)