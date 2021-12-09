from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

urlpatterns = [
    path('api/v1/', include('paymeback.api.urls')),
    path('restricted/', admin.site.urls),
    path('admin/', RedirectView.as_view(url='https://www.djangoproject.com')),
]
