from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse

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