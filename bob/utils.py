import os


def handle_upload_file(f, task_name, filename):
    path = './%s/input/' % task_name
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + filename, 'wb+')as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return os.path.realpath(path + filename)
