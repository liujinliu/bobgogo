import json
from django.http import HttpResponse, HttpResponseRedirect # NOQA
from django.shortcuts import render, get_object_or_404, get_list_or_404 # NOQA
from django.template import loader # NOQA
from django.urls import reverse
from django.utils import timezone
from .models import Tasks, BobTasks


def index(request):
    oldest = Tasks.objects.order_by('cdate')[:1]
    task = oldest[0]
    context = {
        'name': task.name,
        'fields': task.fields.split(","),
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
    # print(bob_task.id)
    # print(bob_task.para)
    return HttpResponseRedirect(reverse('bob:index'))


def bobtasks(request, task_name):
    bobtask = get_list_or_404(BobTasks, name=task_name)
    print(bobtask[0].para)
    print(bobtask[0].status)
    context = {'name': task_name, 'tasks': bobtask}
    return render(request, 'bob/bobtask.html', context)
