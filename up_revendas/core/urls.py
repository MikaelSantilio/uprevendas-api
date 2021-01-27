from django.urls import path
from rest_framework.routers import DefaultRouter

from up_revendas.core import views

app_name = "core"

router = DefaultRouter()

router.register("comprar", views.PurchaseViewSet, basename="purchase")
router.register("vender", views.SaleViewSet, basename="sale")
router.register("contas-bancarias", views.SaleViewSet, basename="bank-account")

urlpatterns = [
    # path("comprar/", views.PurchaseAPIView.as_view(), name="purchase"),
    # path("vender/", views.SaleAPIView.as_view(), name="sale"),
    # path("contas-bancarias/", views.BankAccountListCreateAPIView.as_view(), name="bank-account-list"),
    # path(
    #     "contas-bancarias/<int:pk>/",
    #     views.BankAccountRetrieveUpdateDestroyAPIView.as_view(),
    #     name="bank-account-detail"),
]

urlpatterns += router.urls
