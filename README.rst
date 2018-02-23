bobgogo
=============
bobgogo is a simple Django app to record tasks for you.  
You can create task with diffrent paras via admin page.  
Then users can commit task through the custom page.  

Quick start
~~~~~~~~~~~~~~~
1. Install

::

    # install from pypi
    pip install django-bobgogo
    # install from source
    make build
    make install

1. Add "bob" to your INSTALLED_APPS setting like this

::

    INSTALLED_APPS = [
        ...
        'bob',
    ]

2. Include the URLconf in your project urls.py like this
   
::

    path('bob/', include('bob.urls')),

3. Run `python manage.py migrate` to create the models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a task (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/bob/ and you can see what happened.
