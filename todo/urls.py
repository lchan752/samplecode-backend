from django.urls import path
from todo import views

urlpatterns = [
    path('', views.TaskListCreate.as_view(), name='task_list'),
    path('<int:task_id>/', views.TaskRetrieveUpdateDestroy.as_view(), name='task_detail'),
]