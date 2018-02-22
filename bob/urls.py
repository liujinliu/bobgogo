from django.urls import path

from . import views

app_name = 'bob'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:task_name>/gogo/', views.gogo, name='gogo'),
    path('<str:task_name>/bobtasks/', views.bobtasks, name='bobtasks'),
]
