bobgogo
=============
bobgogo is a simple Django app to record tasks for you.  
You can create task with diffrent paras via admin page.  
Then users can commit task through the custom page.  
`online documention <https://github.com/liujinliu/bobgogo/blob/master/docs/index.md>`_

Quick start
~~~~~~~~~~~~~~~

1. Install

::

    # install from pypi
    pip install django-bobgogo
    # install from source
    make build
    make install

2. Add "bob" to your INSTALLED_APPS setting like this

::

    INSTALLED_APPS = [
        ...
        'bob',
    ]

3. modify the login url in setting

::

    LOGIN_URL = '/bob/'

4. Include the URLconf in your project urls.py like this

::

    path('bob/', include('bob.urls')),

5. Run `python manage.py migrate` to create the models.

5. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a task (you'll need the Admin app enabled).

6. Visit http://127.0.0.1:8000/bob/ and you can see what happened.
