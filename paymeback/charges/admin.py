from django.contrib import admin

from paymeback.core.admin import BaseModelAdmin

from .models import Charge


class ChargeAdmin(BaseModelAdmin):
    pass


admin.site.register(Charge, ChargeAdmin)
