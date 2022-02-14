from django.utils import timezone

from rest_framework import serializers

from .models import Charge


class ChargeSerializer(serializers.ModelSerializer):
    is_late = serializers.SerializerMethodField()

    class Meta:
        model = Charge
        fields = (
            'pk',
            'title',
            'debtor_name',
            'loan_date',
            'date_to_receive',
            'value',
            'debtor_phone',
            'details',
            'debtor',
            'paid',
            'is_late',
        )

    def get_is_late(self, obj):
        return not obj.paid and obj.date_to_receive < timezone.now()
