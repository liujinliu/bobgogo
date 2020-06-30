from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required # NOQA
from .views import task, filedownload, index

app_name = 'bob'
urlpatterns = [
    path('', index.LoginView.as_view(), name='login'),
    path('index', login_required(index.IndexView.as_view()), name='index'),
    path('<str:task_name>/gogo/', task.GogoView.as_view(), name='gogo'),
    path('<str:task_name>/bobtasks/', login_required(task.BobTaskView.as_view()),
         name='bobtasks'),
    path('<str:task_name>/bobtasks/plain/<int:status>/',
         task.BobTaskPlainView.as_view(), name='bobtasks_plaintext'),
    path('<str:task_name>/bobtasks/<int:id>/',
         csrf_exempt(task.BobTaskUpdateView.as_view()), name='bobtasks_update'),
    path('fileload/<str:task_name>/<str:in_out>/<str:filename>/',
         filedownload.file_download, name='file_download'),
]
