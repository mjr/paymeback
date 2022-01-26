from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Charge
from .serializers import ChargeSerializer


class ChargeViewSet(viewsets.ModelViewSet):
    queryset = Charge.objects.all()
    serializer_class = ChargeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.charges.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
