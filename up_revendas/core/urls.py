from django.urls import path

from up_revendas.core import views

app_name = "core"

urlpatterns = [
    path("comprar/", views.PurchaseAPIView.as_view(), name="purchase"),
    path("vender/", views.SaleAPIView.as_view(), name="sale"),
]
