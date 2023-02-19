from django.urls import path, include
from django.conf.urls import url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="TennisBotApi",
        default_version="v1",
    ),
    url="http://127.0.0.1:8000/",
    public=True,
    # permission_classes=[permissions.AllowAny],
    # authentication_classes=[],
)

urlpatterns = [
    path("payments/", include("api.payments.urls")),
    url(
        r"^docs/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
