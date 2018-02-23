import json
from django.http import HttpResponse, HttpResponseRedirect # NOQA
from django.shortcuts import render, get_object_or_404, get_list_or_404 # NOQA
from django.template import loader # NOQA
from django.urls import reverse
from django.utils import timezone
from .models import Tasks, BobTasks


def index(request):
    all_task = Tasks.objects.order_by('cdate')
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


def gogo(request, task_name):
    task = get_object_or_404(Tasks, name=task_name)
    fields = task.fields.split(",") # NOQA
    paras = {}
    for field in fields:
        paras[field] = request.POST[field]
    bob_task = BobTasks(name=task_name, cdate=timezone.now(),
                        udate=timezone.now(), para=json.dumps(paras))
    bob_task.save()
    return HttpResponseRedirect(reverse('bob:bobtasks', args=(task_name,)))


def bobtasks(request, task_name):
    bobtask = get_list_or_404(BobTasks, name=task_name)
    context = {'name': task_name, 'tasks': bobtask}
    return render(request, 'bob/bobtask.html', context)
