from django.urls import path

from up_revendas.cars import views as car_views

app_name = "cars"

urlpatterns = [
    path("", car_views.CarHyperlinkListCreateAPIView.as_view(), name="cars-list"),
    path("<int:pk>", car_views.CarRetrieveUpdateDestroyAPIView.as_view(), name="car-detail"),
    path("marca/", car_views.BrandListCreateAPIView.as_view(), name="brands-list"),
    path("marca/<int:pk>", car_views.BrandRetrieveUpdateDestroyAPIView.as_view(), name="brand-detail"),
    path("modelo/", car_views.ModelListCreateAPIView.as_view(), name="models-list"),
    path("modelo/<int:pk>", car_views.ModelRetrieveUpdateDestroyAPIView.as_view(), name="models-detail"),
    path("choices/", car_views.CarChoicesAPIView.as_view(), name="car-choices"),
]
