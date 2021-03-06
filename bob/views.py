import json
import shutil
import os
import copy
from django.http import HttpResponse, HttpResponseRedirect # NOQA
from django.shortcuts import render, get_object_or_404, get_list_or_404 # NOQA
# pylint: disable=unused-import
from django.template import loader # NOQA
from django.urls import reverse
from django.utils import timezone
from django.http import StreamingHttpResponse
from django.contrib.auth import authenticate, login
from django.views import View
from django.contrib.auth.decorators import login_required # NOQA
from .models import Tasks, BobTasks
from .utils import handle_upload_file


@login_required
def file_download(request, task_name, in_out, filename):
    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    the_file_name = './%s/%s/%s' % (task_name, in_out, filename)
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)
    return response


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
