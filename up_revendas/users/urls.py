from django.urls import path

from up_revendas.users.api import views

app_name = "users"
urlpatterns = [
    path("create-profile/", views.CreateUserAPIView.as_view(), name='create-user'),
    path("activate-store-manager/<int:pk>", views.ActivateStoreManagerAPIView.as_view(), name='activate-store-manager'),
    path("activate-customer/<int:pk>", views.ActivateCustomerAPIView.as_view(), name='activate-customer'),
    path("activate-employee/<int:pk>", views.ActivateEmployeeAPIView.as_view(), name='activate-employee'),
    path("profile/", views.ProfileDetailAPIView.as_view(), name='profile'),
    path("employee-profile/", views.EmployeeDetailAPIView.as_view(), name='employee-profile'),
    path("customer-profile/", views.CustomerDetailAPIView.as_view(), name='customer-profile'),
]
