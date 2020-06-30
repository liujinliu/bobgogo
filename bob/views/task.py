import json
import shutil
import os
import copy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import View
from bob.models import Tasks, BobTasks
from bob.utils import handle_upload_file


class GogoView(View):

    def post(self, request, task_name):
        task = get_object_or_404(Tasks, name=task_name)
        fields = task.fields.split(",") # NOQA
        paras = {}
        for field in fields:
            paras[field] = request.POST[field]
        input_file = ""
        filekey = 'input-file'
        if request.FILES.get(filekey) and str(request.FILES[filekey]):
            input_file = handle_upload_file(request.FILES[filekey], task_name,
                                            str(request.FILES[filekey]))
        bob_task = BobTasks(name=task_name, cdate=timezone.now(),
                            udate=timezone.now(), para=json.dumps(paras),
                            input_file=input_file, output_file="", output="")
        bob_task.save()
        return HttpResponseRedirect(reverse('bob:bobtasks', args=(task_name,)))


class BobTaskView(View):

    def get(self, request, task_name):
        bobtask = get_list_or_404(BobTasks, name=task_name)
        cp_bobtasks = copy.deepcopy(bobtask)
        for t in cp_bobtasks:
            t.input_file = os.path.basename(t.input_file)
        context = {'name': task_name, 'tasks': cp_bobtasks}
        return render(request, 'bob/bobtask.html', context)


class BobTaskPlainView(View):

    def get(self, request, task_name, status):
        bobtask = get_list_or_404(BobTasks, name=task_name, status=status)
        if not bobtask:
            return HttpResponse("no task found")
        ret = []
        for t in bobtask:
            para = json.loads(t.para)
            input_file = t.input_file
            ret.append(dict(id=t.id, para=para, input_file=input_file))
        return HttpResponse(json.dumps(ret))


class BobTaskUpdateView(View):

    def post(self, request, task_name, _id):
        if not request.POST.get("status"):
            return HttpResponse("Error, need status")
        bobtask = get_object_or_404(BobTasks, name=task_name, id=_id)
        if bobtask:
            status = request.POST.get('status', 0)
            bobtask.status = int(status)
            bobtask.output = request.POST.get('output', '')
            output_file_fullpath = request.POST.get('output_file', '')
            filename = os.path.basename(output_file_fullpath)
            target_path = "./%s/output/" % task_name
            if not os.path.exists(target_path):
                os.makedirs(target_path)
            shutil.copy(output_file_fullpath, target_path + filename)
            bobtask.output_file = filename
            bobtask.save()
            return HttpResponse((f"set task:{task_name},id:{_id} status to {status}"
                                 f"output:{bobtask.output}, output_file:{bobtask.output_file}"))
        return HttpResponse("unkonw id")
