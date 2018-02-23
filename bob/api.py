import requests


def fetch_task(host, port, task_name):
    ret = requests.get("http://%s:%d/bob/%s/bobtasks/plain/0/" % (host, port, task_name))
    if ret.status_code == 200:
        return ret.text
    else:
        return None


def update_task(host, port, task_name, id, status):
    para = {'status': 1}
    ret = requests.post("http://%s:%d/bob/%s/bobtasks/%d/"
                        % (host, port, task_name, id), para)
    if ret.status_code == 200:
        return ret.text
    else:
        return None


if __name__ == "__main__":
    fetch_task("127.0.0.1", 8000, "foo")
    # update_task("127.0.0.1", 8000, "foo", 1, 1)
