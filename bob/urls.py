from django.urls import path

from . import views

app_name = 'bob'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:task_name>/gogo/', views.gogo, name='gogo'),
    path('<str:task_name>/bobtasks/', views.bobtasks, name='bobtasks'),
    path('<str:task_name>/bobtasks/plain/<int:status>/',
         views.bobtasks_plaintext, name='bobtasks_plaintext'),
    path('<str:task_name>/bobtasks/<int:id>/',
         views.bobtasks_update, name='bobtasks_update'),
]
