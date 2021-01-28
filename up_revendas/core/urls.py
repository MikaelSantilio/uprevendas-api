from rest_framework.routers import DefaultRouter

from up_revendas.core import views

app_name = "core"

router = DefaultRouter()

router.register("comprar", views.PurchaseViewSet, basename="purchase")
router.register("vender", views.SaleViewSet, basename="sale")
router.register("contas-bancarias", views.BankAccountViewSet, basename="bank-account")

urlpatterns = router.urls
