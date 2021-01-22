from django.urls import path
from up_revendas.core import views


urlpatterns = [
    path("comprar/", views.PurchaseAPIView.as_view(), name="purchase"),
]