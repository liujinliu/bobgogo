from bob.api import BobBox

b = BobBox("127.0.0.1", 8000)
for para in b.query_update("foo", update=False):
    print(para)
