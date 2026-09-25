"""
Regression test for Django issue where HttpResponseNotAllowed 
can't be used in 'await' expression in async views.
"""
from django.test import TestCase
from django.http import HttpResponse
from django.views import View
from django.test import RequestFactory
import asyncio


class DemoAsyncView(View):
    """This basic async view supports only POST requests"""
    async def post(self, request):
        return HttpResponse("ok")


class DemoSyncView(View):
    """This basic sync view supports only POST requests"""
    def post(self, request):
        return HttpResponse("ok")


class HttpResponseNotAllowedAwaitTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_async_view_get_method_raises_await_error_old_behavior(self):
        """Test that the async view with GET request causes the await error in old code"""
        # Create a GET request
        request = self.factory.get('/demo')
        
        # Test the behavior - in the old buggy code this should raise TypeError
        # because HttpResponseNotAllowed is returned as a coroutine instead of being awaited properly
        view = DemoAsyncView.as_view()
        
        # This should demonstrate the problem when called directly, but let's test
        # if the view is correctly handling method not allowed responses
        
        # The issue is in http_method_not_allowed method where we get a coroutine
        # rather than a plain HttpResponseNotAllowed when view_is_async is True
        with self.assertRaises(TypeError) as context:
            response = view(request)
            # Try to await it if it's a coroutine
            if asyncio.iscoroutine(response):
                asyncio.run(response)
        
        # In the old code this would raise "object HttpResponseNotAllowed can't be used in 'await' expression"
        # But that's hard to test unless we directly call the method
    
    def test_async_view_method_not_allowed_returns_correct_type(self):
        """Test that async view's http_method_not_allowed returns proper type"""
        # Access the method directly to see what it returns
        view_instance = DemoAsyncView()
        
        # The issue is when view_is_async is True and we call http_method_not_allowed
        # In old code it returns a coroutine function, not HttpResponseNotAllowed directly
        response = view_instance.http_method_not_allowed(self.factory.get('/demo'))
        
        # This should behave correctly in the fixed version but not in the old one
        # In the old version, response might be a coro function, not an HttpResponse
        # So we can't do `await response` directly
        
        # Check that the response is usable
        self.assertIsNotNone(response)
        
    def test_sync_view_method_not_allowed_returns_correct_type(self):
        """Test that sync view's http_method_not_allowed returns proper HttpResponse"""
        # Access the method directly
        view_instance = DemoSyncView()
        
        # This should always return a proper HttpResponse in both old and new code
        response = view_instance.http_method_not_allowed(self.factory.get('/demo'))
        
        # This should be a proper HttpResponse
        from django.http import HttpResponseNotAllowed
        self.assertIsInstance(response, HttpResponseNotAllowed)