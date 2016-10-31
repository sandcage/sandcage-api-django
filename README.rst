django-sandcage is an demo app of Django UI to SandCage's API. The API documentation can be found at `SandCage's API documentation <https://www.sandcage.com/docs/0.2/>`_


Table of Contents
-----------------
* `Requirements <https://github.com/sandcage/sandcage-api-django/tree/dev#requirements>`_
* `Installation <https://github.com/sandcage/sandcage-api-django/tree/dev#installation>`_
* `Usage <https://github.com/sandcage/sandcage-api-django/tree/dev#usage>`_
* `Contributing <https://github.com/sandcage/sandcage-api-django/tree/dev#contributing>`_
* `Contact Us <https://www.sandcage.com/contact>`_



Requirements
------------
- Django==1.10.2
- certifi==2016.9.26
- django-appconf==1.0.2
- django-bootstrap3==7.1.0
- django-compressor==2.1
- django-libsass==0.7
- django-sass-processor==0.5.1
- libsass==0.11.2
- rcssmin==1.0.6
- requests==2.11.1
- rjsmin==1.0.12
- sandcage==0.2.0
- six==1.10.0

In order to make use of the software you need a SandCage API Key. Once logged into SandCage, you can get your API Key from `here <https://www.sandcage.com/panel/api_key>`_.

Installation
-------
This example is using virtual environment (this is not the only possible way to go)::

  virtualenv -p python3 virtual3
  cd virtual3
  source bin/activate
  git clone path_to_package
  cd sandcage-django
  pip install -r requirements.txt
  cd src
  python manage.py migrate

  
Usage
-----

Run the Django test server at source code directory by::

  python manage.py runserver

Then navigate to address http://127.0.0.1:8000
  
Contributing
------------

We are open to suggestions and code revisions, however there are some rules and limitations that you might want to consider first.

- Code that you contribute will automatically be licensed under the `Apache License Version 2.0 <https://github.com/sandcage/sandcage-api-python/blob/master/LICENSE>`_.
- Third party code will be reviewed, tested and possibly modified before being released.

These basic rules help ensure that this code remains Open Source and compatible with Apache 2.0 license. All contributions will be added to the changelog and appear in every release.
