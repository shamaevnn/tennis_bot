from rest_framework.routers import DefaultRouter

from api.payments.views import PaymentsViewSet

urlpatterns = []


router = DefaultRouter()
router.register(r"", PaymentsViewSet, basename="cities")


urlpatterns += router.urls
