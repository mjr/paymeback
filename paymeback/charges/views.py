from django.shortcuts import render

from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Charge
from .serializers import ChargeSerializer


class ChargeFilter(FilterSet):
    class Meta:
        model = Charge
        fields = {
            'title': ['exact', 'contains'],
            'debtor_name': ['exact', 'contains'],
            'loan_date': ['exact', 'range'],
            'date_to_receive': ['exact', 'range'],
            'value': ['exact', 'range'],
            'paid': ['exact'],
        }


class ChargeViewSet(viewsets.ModelViewSet):
    queryset = Charge.objects.all()
    serializer_class = ChargeSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = ChargeFilter

    def get_queryset(self):
        return self.request.user.charges.filter(deleted__isnull=True)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
