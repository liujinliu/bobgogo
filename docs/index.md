## Bobgogo
bobgogo是一款用于对任务进行简单记录的工具, 部署之后是一个网站. 通过这个网站运营人员可以发布任务, 任务发布后, 可以在网站看到任务的状态(0表示任务未处理, 1表示任务已处理). 同时bobgogo提供编程接口给开发人员, 用于获取特定的任务(接口返回任务参数, 处理后会自动将任务置为已处理状态, 并可在网页显示出更新后的状态.
### 部署和启动
#### 1. 安装bobgogo
```
# 首先安装django
pip install django

#安装bobgogo

# via pip
pip install django-bobgogo

# 通过源码安装
git clone https://github.com/liujinliu/bobgogo.git
cd bobgogo
make install
```

#### 2. 部署网站
```
#新建django项目(如果已有自己的django项目, 此步骤可以忽略)
django-admin startproject mysite
```
修改mysite的settings.py如下:  
```
# Application definition
INSTALLED_APPS = [
    'bob',
    .......,
]
```
在urls.py中加入如下内容:  
```
urlpatterns = [
    path('bob/', include('bob.urls')),
    .......,
]
```
执行下面的命令建立相关的数据表:  
```
python manage.py migrate
```
通过下面的命令创建管理员:  
```
python manage.py createsuperuser
```
启动网站
```
python manage.py runserver
```
打开http://127.0.0.1:8000/bob, 可以看到如下的页面:  
![](https://github.com/liujinliu/bobgogo/raw/master/docs/imgs/first_start.png)  
哈哈, 部署成功! 下面我们来看如何使用.  

### 创建Task
task由开发人员来创建, 首先打开admin页面:  
![](https://github.com/liujinliu/bobgogo/raw/master/docs/imgs/admin.png)  
点击右下角的Add按钮新建Task, 如下所示:  
![](https://github.com/liujinliu/bobgogo/raw/master/docs/imgs/add_task.png)  
点击Save按钮. 此时返回http://127.0.0.1:8000/bob, 点击相应的Tab(此时为foo)可以看到下面的页面:  
![](https://github.com/liujinliu/bobgogo/raw/master/docs/imgs/foo.png)  
我们可以重复上面的步骤, 创建不同种类的Task

### 提交Task
在对应的输入框中输入内容, 如下所示:  
![](https://github.com/liujinliu/bobgogo/raw/master/docs/imgs/Iloveanan.png)  
点击Save, 可以看到页面跳转之后如下:  
![](https://github.com/liujinliu/bobgogo/raw/master/docs/imgs/bobtasks.png)  
可以重复上面的步骤, 在foo下创建多个任务记录.
![](https://github.com/liujinliu/bobgogo/raw/master/docs/imgs/bobtask2.png)  

### 编程接口的使用
参考下面的例子:
```
from bob.api import BobBox

b = BobBox("127.0.0.1", 8000)

# update参数为True时, 在每次处理之后, 这一条task数据的status会自动更新为1, 那么下一次调用
# query_update这个迭代器则已经处理过的这一条不会再返回
# 如果想自己手动更新的话, 这里传成False, 默认为False
for para in b.query_update("foo", update=False):
    print(para) # do something to the task
```
运行后得到结果如下:
```
{'bar0': 'I', 'bar1': 'love', 'bar2': 'anan'}
{'bar0': 'everyone', 'bar1': 'love', 'bar2': 'bob'}
```
