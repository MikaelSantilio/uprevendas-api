from django.conf import settings
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter, SimpleRouter

from up_revendas.cars import views as car_views
from up_revendas.core import views
from up_revendas.users.api.views import UserViewSet

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

app_name = "api"

router.register("users", UserViewSet)

urlpatterns = [
    # url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("redoc/", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("comprar/", views.PurchaseAPIView.as_view(), name="purchase"),
    path("vender/", views.SaleAPIView.as_view(), name="sale"),
    path("carros/", car_views.CarHyperlinkListCreateAPIView.as_view(), name="cars"),
    path("carros/<int:pk>", car_views.CarRetrieveUpdateDestroyAPIView.as_view(), name="car-detail"),
]

urlpatterns += router.urls
