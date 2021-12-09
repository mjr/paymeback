from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin


admin.site.enable_nav_sidebar = False


class BaseModelAdmin(SimpleHistoryAdmin):
    readonly_fields = ('created', 'modified', 'deleted')
    list_per_page = 10
