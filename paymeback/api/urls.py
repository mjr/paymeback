from django.urls import include, path

from rest_framework import routers

from paymeback.charges.views import ChargeViewSet
from paymeback.users.views import RegisterView, TokenView

router = routers.SimpleRouter()
router.register(r'charges', ChargeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', TokenView.as_view()),
    path('register/', RegisterView.as_view()),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
