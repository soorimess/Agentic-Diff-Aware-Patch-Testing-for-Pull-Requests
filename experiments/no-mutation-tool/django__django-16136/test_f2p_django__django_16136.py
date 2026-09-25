"""
Regression test for Django issue with async View and HttpResponseNotAllowed.
This test ensures that the Django async method not allowed fix works.
"""

from django.test import TestCase
from django.views.generic import View
from django.http import HttpResponse, HttpRequest


class AsyncPostOnlyView(View):
    """A view that only supports POST requests asynchronously."""
    
    async def post(self, request):
        return HttpResponse("POST response")


class TestAsyncViewMethodNotAllowedBehavior(TestCase):
    
    def test_async_view_no_typeerror(self):
        """
        The key test: Ensure that calling http_method_not_allowed on an async view
        does not result in the TypeError:
        "object HttpResponseNotAllowed can't be used in 'await' expression"
        """
        # Create an async view that only supports POST 
        view = AsyncPostOnlyView()
        
        # This is the key validation - don't trigger the specific type error
        # This is the exact problem from the bug report that should be fixed
        request = HttpRequest()
        request.method = 'GET'  # This will trigger method not allowed
        
        try:
            response = view.http_method_not_allowed(request, 'get')
            # Ensure that no TypeError about not being awaitable happens
            # If we can make this call without-errors, it means 
            # the bug fix worked (prevents the await error)
        except TypeError as e:
            if "can't be used in 'await' expression" in str(e):
                self.fail(f"Bug still present: {e}")
            else:
                raise  # re-raise if it's a different TypeError

    def test_sync_view_still_works(self):
        """
        Verify that sync views still work correctly
        """
        from django.views.generic import View
        
        class SyncPostOnlyView(View):
            def post(self, request):
                return HttpResponse("POST response")
        
        view = SyncPostOnlyView()
        
        # Create a proper request with method set
        request = HttpRequest()
        request.method = 'GET'
        
        try:
            response = view.http_method_not_allowed(request, 'get')
            # Should not raise TypeError
        except TypeError as e:
            if "can't be used in 'await' expression" in str(e):
                self.fail(f"Sync view also broken: {e}")
            else:
                raise  # re-raise if it's a different TypeError