from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.views import View
from bob.models import Tasks


class LoginView(View):

    def get(self, request):
        return render(request, 'bob/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('bob:index',))
        return HttpResponseRedirect(reverse('bob:login',))


class IndexView(View):
    def get(self, request):
        # pylint: disable=no-member
        all_task = Tasks.objects.order_by('cdate')
        if len(all_task) > 0:
            t = all_task[0]
            all_t = []
            for t in all_task:
                all_t.append(dict(current_name=t.name,
                                  current_fields=t.fields.split(",")))
            context = {
                'all_names': list(map(lambda x: x.name, all_task)),
                'all_t': all_t
            }
            return render(request, 'bob/index.html', context)
        return HttpResponse("No Task found, first add a task via admin page")