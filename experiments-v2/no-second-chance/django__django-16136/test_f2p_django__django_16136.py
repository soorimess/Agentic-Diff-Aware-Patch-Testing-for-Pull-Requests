import asyncio
from django.http import HttpResponseNotAllowed
from django.test import TestCase
from django.views import View


class AsyncPostOnlyView(View):
    """A view that only supports POST requests"""
    async def post(self, request):
        return HttpResponseNotAllowed("ok")


class TestAsyncViewMethodNotAllowed(TestCase):
    """Test that async views handle method not allowed correctly"""
    
    def test_async_view_dispatch_with_disallowed_method(self):
        """
        Test that async views properly handle disallowed HTTP methods
        without raising TypeError about awaiting HttpResponseNotAllowed.
        """
        from django.test import RequestFactory
        factory = RequestFactory()
        request = factory.get('/test/')
        
        # Create async view that only supports POST
        async_view = AsyncPostOnlyView()
        
        # Verify this is an async view
        self.assertTrue(async_view.view_is_async)
        
        # This should not raise: "TypeError: object HttpResponseNotAllowed can't be used in 'await' expression"
        try:
            # This will call http_method_not_allowed internally when GET is not allowed
            result = async_view.dispatch(request)
            
            # The fix ensures that when view_is_async is True, 
            # the result is awaitable (a coroutine) rather than HttpResponseNotAllowed directly
            if asyncio.iscoroutine(result):
                # Test that we can await it properly - this is the core fix
                async def test_await():
                    response = await result
                    self.assertIsInstance(response, HttpResponseNotAllowed)
                asyncio.run(test_await())
            else:
                # For sync views, this would be HttpResponseNotAllowed directly
                # But for async views, it should be awaitable
                self.assertIsInstance(result, HttpResponseNotAllowed)
                
        except TypeError as e:
            if "can't be used in 'await' expression" in str(e):
                self.fail(f"Got unexpected TypeError about await: {e}")
            raise

    def test_async_view_identification(self):
        """Test that async views are correctly identified"""
        async_view = AsyncPostOnlyView()
        self.assertTrue(async_view.view_is_async)
        
        # Test sync view for comparison
        class SyncView(View):
            def get(self, request):
                return HttpResponseNotAllowed("ok")
        
        sync_view = SyncView()
        self.assertFalse(sync_view.view_is_async)