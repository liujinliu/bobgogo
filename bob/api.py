import requests
import json


class BobBox(object):

    def __init__(self, host="127.0.0.1", port=8000):
        self.host = host
        self.port = port

    def fetch_task(self, task_name, status):
        ret = requests.get("http://%s:%d/bob/%s/bobtasks/plain/%d/"
                           % (self.host, self.port, task_name, status))
        if ret.status_code == 200:
            return ret.text
        else:
            return None

    def update_task(self, task_name, id, status):
        para = {'status': 1}
        ret = requests.post("http://%s:%d/bob/%s/bobtasks/%d/"
                            % (self.host, self.port, task_name, id), para)
        if ret.status_code == 200:
            return ret.text
        else:
            return None

    def query_update(self, task_name, update=False):
        tasks = self.fetch_task(task_name, 0)
        if tasks:
            tmp = json.loads(tasks)
            for t in tmp:
                yield t["para"]
                if update:
                    self.update_task(task_name, t["id"], 1)


if __name__ == "__main__":
    b = BobBox("127.0.0.1", 8000)
    for para in b.query_update("foo"):
        print(para)
