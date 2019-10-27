from django.urls import path
from users import views

urlpatterns = [
    path('', views.UserList.as_view(), name='user_list'),
    path('create/', views.UserCreate.as_view(), name='user_create'),
]