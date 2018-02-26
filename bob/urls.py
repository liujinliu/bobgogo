from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

app_name = 'bob'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<str:task_name>/gogo/', views.GogoView.as_view(), name='gogo'),
    path('<str:task_name>/bobtasks/', views.BobTaskView.as_view(), name='bobtasks'),
    path('<str:task_name>/bobtasks/plain/<int:status>/',
         views.BobTaskPlainView.as_view(), name='bobtasks_plaintext'),
    path('<str:task_name>/bobtasks/<int:id>/',
         csrf_exempt(views.BobTaskUpdateView.as_view()), name='bobtasks_update'),
    path('fileload/<str:task_name>/<str:in_out>/<str:filename>/',
         views.file_download, name='file_download'),
]
