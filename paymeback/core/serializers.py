from rest_framework import serializers

from paymeback.charges.serializers import ChargeSerializer
from paymeback.core.utils import format_currency
from paymeback.users.models import User


class InsightSerializer(serializers.ModelSerializer):
    late_amount = serializers.SerializerMethodField()
    total_amount_borrowed = serializers.SerializerMethodField()
    charges = ChargeSerializer(many=True)

    class Meta:
        model = User
        fields = (
            'late_amount',
            'total_amount_borrowed',
            'charges',
        )

    def get_late_amount(self, obj):
        return format_currency(obj.get_late_amount())

    def get_total_amount_borrowed(self, obj):
        return format_currency(obj.get_total_amount_borrowed())
