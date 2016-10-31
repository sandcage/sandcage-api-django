.. image:: https://d18m5nnl28b2pp.cloudfront.net/p/a/img/header.png

-------------------------------------------------------------------


.. image:: https://scrutinizer-ci.com/g/sandcage/sandcage-api-python/badges/quality-score.png?b=master
    :target: https://scrutinizer-ci.com/g/sandcage/sandcage-api-python/?branch=master
.. image:: https://travis-ci.org/sandcage/sandcage-api-python.svg?branch=master
    :target: https://travis-ci.org/sandcage/sandcage-api-python

django-sandcage is an demo app of Django UI to SandCage's API. The API documentation can be found at `SandCage's API documentation <https://www.sandcage.com/docs/0.2/>`_


Table of Contents
-----------------
* `Requirements <https://github.com/sandcage/sandcage-api-python#requirements>`_
* `Installation <https://github.com/sandcage/sandcage-api-python#install>`_
* `Usage <https://github.com/sandcage/sandcage-api-python#usage>`_
* `Examples <https://github.com/sandcage/sandcage-api-python/tree/master/examples>`_
* `Contributing <https://github.com/sandcage/sandcage-api-python#contributing>`_
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

Install
-------
This example is using virtual environment (this is not the only possible way to go)::

  virtualenv -p python3 virtual3
  cd virtual3
  source bin/activate
  git clone path_to_package
  
Using pip::

  pip install sandcage

or alternatively clone and install::

  git clone https://github.com/sandcage/sandcage-api-python
  cd sandcage-api-python
  python setup.py install

Usage
-----

Simply::
  
  from sandcage import SandCage

  sc = SandCage('[YOUR_SANDCAGE_API_KEY]')
  sc.list_files_service()

See more `examples <https://github.com/sandcage/sandcage-api-python/tree/master/examples>`_

To not include YOUR_SANDCAGE_API_KEY into your code you can for example save it as a file named SANDCAGE_API_KEY into your home directory::

  cd ~
  echo YOUR_SANDCAGE_API_KEY > SANDCAGE_API_KEY

and then use the following code to initialize SandCage::

  import os.path
  from sandcage import SandCage

  api_key_dir = os.path.expanduser('~')
  api_key_file = os.path.join(api_key_dir, 'SANDCAGE_API_KEY')
  with open(api_key_file, 'r') as f:
      api_key = f.readline()

  sc = SandCage(api_key=api_key)

Contributing
------------

We are open to suggestions and code revisions, however there are some rules and limitations that you might want to consider first.

- Code that you contribute will automatically be licensed under the `Apache License Version 2.0 <https://github.com/sandcage/sandcage-api-python/blob/master/LICENSE>`_.
- Third party code will be reviewed, tested and possibly modified before being released.

These basic rules help ensure that this code remains Open Source and compatible with Apache 2.0 license. All contributions will be added to the changelog and appear in every release.
