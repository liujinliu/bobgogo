from bob.api import BobBox

b = BobBox("127.0.0.1", 8000)
for para in b.query_update("foo", update=False):
    print(para)
    b.update_task("foo", para['id'], 0, 0, "/home/liujinliu/bot.csv")
