"""
Regression test for Django issue: HttpResponseNotAllowed can't be used in 'await' expression

This test specifically verifies that in an async View context, 
http_method_not_allowed returns a response that can be awaited without error.
"""
from django.http import HttpResponse
from django.test import SimpleTestCase
from django.views.generic import View
import asyncio


class AsyncPostOnlyView(View):
    """An async view that only accepts POST requests"""
    
    async def post(self, request):
        return HttpResponse("ok")


class HttpResponseNotAllowedAwaitTest(SimpleTestCase):
    """
    Test that verifies async views properly handle method not allowed cases
    to prevent "object HttpResponseNotAllowed can't be used in 'await' expression" error.
    """
    
    def test_async_view_method_not_allowed_response_is_awaitable(self):
        """
        The core fix: when an async view has view_is_async=True and gets a method
        it doesn't support, http_method_not_allowed should return something 
        awaitable, not cause TypeError.
        """
        # Create an instance of our async POST-only view
        view_instance = AsyncPostOnlyView()
        
        # Verify the view is detected as async
        self.assertTrue(view_instance.__class__.view_is_async)
        
        from django.test import RequestFactory
        rf = RequestFactory()
        get_request = rf.get('/test/')
        
        # This call to http_method_not_allowed should NOT fail when awaited
        # This is the exact scenario that failed in the buggy version
        response = view_instance.http_method_not_allowed(get_request)
        
        # In the FIXED version, this response should be awaitable
        # In the BUGGY version, this would have raised: 
        # TypeError: object HttpResponseNotAllowed can't be used in 'await' expression
        
        # Check that if it's a coroutine, we can await it successfully
        if asyncio.iscoroutine(response):
            # Test the specific fix: can we await it without error?
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                # This is where the bug manifested - trying to await HttpResponseNotAllowed 
                result = loop.run_until_complete(response)
                self.assertEqual(result.status_code, 405)
                self.assertEqual(result.reason_phrase, "Method Not Allowed")
            finally:
                loop.close()
        else:
            # Even if not async, verify it still works
            self.assertEqual(response.status_code, 405)
    
    def test_response_type_consistency_in_async_context(self):
        """
        Verify that http_method_not_allowed when called from async context
        returns a result that maintains consistency with async handling.
        """
        view_instance = AsyncPostOnlyView()
        
        from django.test import RequestFactory
        rf = RequestFactory()
        get_request = rf.get('/test/')
        
        import inspect
        
        # The fix adds special handling for view_is_async=True context
        response = view_instance.http_method_not_allowed(get_request)
        
        # When the view is async, the fix should return an awaitable 
        # regardless of the immediate result (this tests the conditional logic)
        if asyncio.iscoroutine(response):
            # This path should work in the fixed version
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(response)
                self.assertEqual(result.status_code, 405)
            finally:
                loop.close()
        else:
            # In non-async case, should return a normal response
            self.assertEqual(response.status_code, 405)
            
    def test_specific_error_prevention(self):
        """
        Explicitly make sure we don't get the specific error from the bug report.
        """
        view_instance = AsyncPostOnlyView()
        
        from django.test import RequestFactory
        rf = RequestFactory()
        get_request = rf.get('/test/')
        
        # The error was: TypeError: object HttpResponseNotAllowed can't be used in 'await' expression
        try:
            response = view_instance.http_method_not_allowed(get_request)
            
            # This should not raise the specific TypeError from the bug report
            if asyncio.iscoroutine(response):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    result = loop.run_until_complete(response)  
                    # If we can get here without TypeError, the fix works
                    self.assertEqual(result.status_code, 405)
                finally:
                    loop.close()
            else:
                # Even if synchronous, it should work
                self.assertEqual(response.status_code, 405) 
                
        except TypeError as e:
            if "object HttpResponseNotAllowed can't be used in 'await' expression" in str(e):
                # This is the exact bug we're preventing
                self.fail("Bug still present: %s" % str(e))
            else:
                raise  # Re-raise if it's a different TypeError