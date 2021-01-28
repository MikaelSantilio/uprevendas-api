from django.urls import path
from rest_framework.routers import DefaultRouter

from up_revendas.cars import views as car_views

app_name = "cars"

router = DefaultRouter()
router.register("", car_views.CarViewSet, basename="cars")

urlpatterns = [
    path("marca/", car_views.BrandListCreateAPIView.as_view(), name="brands-list"),
    path("marca/<int:pk>/", car_views.BrandRetrieveUpdateDestroyAPIView.as_view(), name="brand-detail"),
    path("modelo/", car_views.ModelListCreateAPIView.as_view(), name="models-list"),
    path("modelo/<int:pk>/", car_views.ModelRetrieveUpdateDestroyAPIView.as_view(), name="models-detail"),
]

urlpatterns += router.urls
