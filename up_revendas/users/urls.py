from django.urls import path

from up_revendas.users import views

app_name = "users"
urlpatterns = [
    path("funcoes/", views.FunctionListCreateAPIView.as_view(), name='functions-list'),
    path("funcoes/<int:pk>/", views.FunctionRetrieveUpdateDestroyAPIView.as_view(), name='function-detail'),

    path("criar-perfil/", views.CreateUserAPIView.as_view(), name='create-user'),
    path("ativar-gerente-loja/<int:pk>/", views.ActivateStoreManagerAPIView.as_view(), name='activate-store-manager'),
    path("ativar-cliente/<int:pk>/", views.ActivateCustomerAPIView.as_view(), name='activate-customer'),
    path("ativar-funcionario/<int:pk>/", views.ActivateEmployeeAPIView.as_view(), name='activate-employee'),

    path("lista-vendedores/", views.SellersListAPIView.as_view(), name='sellers-list'),
    path("lista-clientes/", views.CustomersListAPIView.as_view(), name='customers-list'),
    path("lista-usuarios/", views.UserListAPIView.as_view(), name='users-list'),

    path("meu-perfil/", views.MyProfileAPIView.as_view(), name='my-profile'),
    path("perfil/<int:pk>/", views.ProfileDetailAPIView.as_view(), name='profile-detail'),
]
