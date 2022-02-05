from rest_framework import serializers

from .models import Charge


class ChargeSerializer(serializers.ModelSerializer):
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
        )
