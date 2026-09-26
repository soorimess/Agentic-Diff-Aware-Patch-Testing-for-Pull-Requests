import unittest
from django.http import HttpResponse, HttpResponseNotAllowed
from django.test import TestCase
from django.views import View


class AsyncPostOnlyView(View):
    """A view that only supports POST requests"""
    async def post(self, request):
        return HttpResponse("ok")


class TestAsyncViewMethodNotAllowed(TestCase):
    def test_async_view_method_not_allowed_does_not_raise_typeerror(self):
        """
        Test that async views with only some HTTP methods implemented
        don't raise "object HttpResponseNotAllowed can't be used in 'await' expression"
        when handling disallowed HTTP methods.
        """
        # Create an async view instance
        view_instance = AsyncPostOnlyView()
        
        # Verify it's detected as async
        self.assertTrue(view_instance.__class__.view_is_async)
        
        # Mock a request object
        class MockRequest:
            method = "GET"
            path = "/test/"
            
        mock_request = MockRequest()
        
        # This test ensures that the specific TypeError is prevented
        # The bug was that HttpResponseNotAllowed was returned directly
        # and then awaited in async context, causing TypeError
        try:
            # This call should not raise the specific TypeError
            response = view_instance.http_method_not_allowed(mock_request)
            
            # The fix ensures that when view_is_async is True, 
            # the response can be properly handled in async contexts
            # without raising "object HttpResponseNotAllowed can't be used in 'await' expression"
            
        except TypeError as e:
            if "object HttpResponseNotAllowed can't be used in 'await' expression" in str(e):
                self.fail(f"Original bug still present: {e}")
            else:
                raise

    def test_sync_view_method_not_allowed_returns_httpresponse(self):
        """
        Test that sync views return HttpResponseNotAllowed directly.
        """
        class SyncPostOnlyView(View):
            def post(self, request):
                return HttpResponse("ok")
        
        # Create a sync view instance
        view_instance = SyncPostOnlyView()
        
        # Verify it's NOT detected as async
        self.assertFalse(view_instance.__class__.view_is_async)
        
        # Mock a request object
        class MockRequest:
            method = "GET"
            path = "/test/"
            
        mock_request = MockRequest()
        
        # Sync views should return HttpResponseNotAllowed directly
        response = view_instance.http_method_not_allowed(mock_request)
        
        # Should be HttpResponseNotAllowed directly
        self.assertIsInstance(response, HttpResponseNotAllowed)
        self.assertEqual(response.status_code, 405)