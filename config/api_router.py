from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter
from up_revendas.core import views

from up_revendas.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

app_name = "api"

router.register("users", UserViewSet)

urlpatterns = [
    path("comprar/", views.PurchaseAPIView.as_view(), name="purchase"),
    path("vender/", views.SaleAPIView.as_view(), name="sale"),
]

urlpatterns += router.urls
