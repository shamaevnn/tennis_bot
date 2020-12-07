from django.shortcuts import redirect

# Create your views here.

from django.http import HttpResponseNotFound, HttpResponseServerError
from sentry_sdk import capture_message


def my_custom_page_not_found_view(*args, **kwargs):
    capture_message("Page not found!", level="error")

    # return any response here, e.g.:
    return HttpResponseNotFound("Not found")


def my_custom_error_view(*args, **kwargs):
    capture_message("Page not found!", level="error")

    # return any response here, e.g.:
    return HttpResponseServerError("Error on server")


def home_redirect(request):
    return redirect('admin/base/')
