from rest_framework import mixins, viewsets, status
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from api.payments.serializaers import GetPaymentSerializer
from base.models import Payment

group_id_param = openapi.Parameter('group_id', openapi.IN_QUERY, type=openapi.TYPE_NUMBER, required=True)
month_param = openapi.Parameter('month', openapi.IN_QUERY, type=openapi.TYPE_NUMBER, required=True, enum=Payment.available_months())
year_param = openapi.Parameter('year', openapi.IN_QUERY, type=openapi.TYPE_NUMBER, required=True, enum=Payment.available_years())


class PaymentsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = GetPaymentSerializer

    @swagger_auto_schema(manual_parameters=[group_id_param, month_param, year_param])
    def list(self, request, *args, **kwargs):
        """

        """
        params = request.query_params
        group_id = params.get("group_id")
        month = params.get("month")
        year = params.get("year")

        if not all((group_id, month, year)):
            return JsonResponse(
                data={'error': 'Required params are missing'},
                status=status.HTTP_400_BAD_REQUEST
            )

        payments = Payment.objects.filter(
            player__traininggroup__id=group_id, month=month, year=year
        )
        serializer = self.serializer_class(payments, many=True)
        return JsonResponse({"payments": serializer.data})
