from django.urls import include, path

from rest_framework import routers

from paymeback.charges.views import ChargeViewSet


router = routers.SimpleRouter()
router.register(r'charges', ChargeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
