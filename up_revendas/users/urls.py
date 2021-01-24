from django.urls import path

from up_revendas.users.api import views

app_name = "users"
urlpatterns = [
    path("functions/", views.FunctionListCreateAPIView.as_view(), name='functions-list'),
    path("functions/<int:pk>/", views.FunctionRetrieveUpdateDestroyAPIView.as_view(), name='function-detail'),

    path("create-profile/", views.CreateUserAPIView.as_view(), name='create-user'),
    path("activate-store-manager/<int:pk>/", views.ActivateStoreManagerAPIView.as_view(), name='activate-store-manager'),
    path("activate-customer/<int:pk>/", views.ActivateCustomerAPIView.as_view(), name='activate-customer'),
    path("activate-employee/<int:pk>/", views.ActivateEmployeeAPIView.as_view(), name='activate-employee'),

    path("sellers-list/", views.SellersListAPIView.as_view(), name='sellers-list'),
    path("customers-list/", views.CustomersListAPIView.as_view(), name='customers-list'),

    path("my-profile/", views.MyProfileAPIView.as_view(), name='my-profile'),
    path("profile/<int:pk>/", views.ProfileDetailAPIView.as_view(), name='profile-detail'),
    path("employee-profile/", views.EmployeeDetailAPIView.as_view(), name='employee-profile'),
    path("customer-profile/", views.CustomerDetailAPIView.as_view(), name='customer-profile'),
]
