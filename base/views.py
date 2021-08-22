import json
from django.shortcuts import redirect
from django.views import View
from django.http import JsonResponse

from django.http import HttpResponseNotFound, HttpResponseServerError
from sentry_sdk import capture_message

from admin_bot.main import process_admin_telegram_event
from player_bot.main import process_telegram_event
from tennis_bot.settings import DEBUG


def my_custom_page_not_found_view(*args, **kwargs):
    capture_message("Page not found!", level="error")

    # return any response here, e.g.:
    return HttpResponseNotFound("Not found")


def my_custom_error_view(*args, **kwargs):
    capture_message("Page not found!", level="error")

    # return any response here, e.g.:
    return HttpResponseServerError("Error on server")


def home_redirect(request):
    return redirect('tgadmin/base/')


class TelegramBotWebhookView(View):
    # WARNING: if fail - Telegram webhook will be delivered again.
    # Can be fixed with async celery task execution
    def post(self, request, *args, **kwargs):
        if DEBUG:
            process_telegram_event(json.loads(request.body))
        else:  # use celery in production
            process_telegram_event.delay(json.loads(request.body))

        return JsonResponse({"ok": "POST request processed"})

    def get(self, request, *args, **kwargs):  # for debug
        return JsonResponse({"ok": "Get request processed. But nothing done"})


class TelegramAdminBotWebhookView(View):
    # WARNING: if fail - Telegram webhook will be delivered again.
    # Can be fixed with async celery task execution
    def post(self, request, *args, **kwargs):
        if DEBUG:
            process_admin_telegram_event(json.loads(request.body))
        else:  # use celery in production
            process_admin_telegram_event.delay(json.loads(request.body))

        return JsonResponse({"ok": "POST request processed"})

    def get(self, request, *args, **kwargs):  # for debug
        return JsonResponse({"ok": "Get request processed. But nothing done"})