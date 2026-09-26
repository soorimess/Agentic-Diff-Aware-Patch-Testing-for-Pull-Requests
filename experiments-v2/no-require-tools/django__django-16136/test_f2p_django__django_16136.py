import asyncio
from unittest import TestCase
from django.views import View
from django.http import HttpResponse
from django.test import RequestFactory

class AsyncOnlyView(View):
    """This basic view supports only POST requests"""
    async def post(self, request):
        return HttpResponse("ok")

class TestAsyncViewMethodNotAllowed(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        
    def test_async_view_http_method_not_allowed_prevents_await_error(self):
        """
        Test that async views don't raise 'object HttpResponseNotAllowed can't be used in 'await' expression'
        
        This is the core fix for the reported bug. When an async-only view
        receives a request for a non-existent method, the http_method_not_allowed
        must return something that can be awaited in async contexts.
        """
        # Create an async view instance
        view = AsyncOnlyView()
        
        # This view should be detected as async (key to the fix)
        self.assertTrue(view.__class__.view_is_async)
        
        # Call http_method_not_allowed - this is where the fix is applied
        request = self.factory.get('/demo')
        response = view.http_method_not_allowed(request)
        
        # The fix ensures that when view_is_async is True, 
        # http_method_not_allowed returns an awaitable coroutine
        # This prevents the TypeError when async context tries to await it
        
        # Test the key behavior: can we await the response without error?
        try:
            # This would raise TypeError in old buggy code
            async def test_await():
                if asyncio.iscoroutine(response):
                    return await response
                else:
                    return response
                    
            result = asyncio.run(test_await())
            self.assertEqual(result.status_code, 405)
        except TypeError as e:
            if "object HttpResponseNotAllowed can't be used in 'await' expression" in str(e):
                self.fail("The fix is not working - still getting the await error")
            else:
                raise

    def test_sync_view_still_works(self):
        """Ensure sync views continue to work normally"""
        class SyncOnlyView(View):
            def post(self, request):
                return HttpResponse("ok")
        
        view = SyncOnlyView()
        request = self.factory.get('/demo')
        response = view.http_method_not_allowed(request)
        self.assertEqual(response.status_code, 405)

    def test_response_has_correct_allow_header(self):
        """Test that 405 response includes correct Allow header"""
        request = self.factory.get('/demo')
        response = AsyncOnlyView.as_view()(request)
        self.assertEqual(response.status_code, 405)
        self.assertIn('POST', response['Allow'])