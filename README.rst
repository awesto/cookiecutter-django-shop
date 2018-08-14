Cookiecutter for django-SHOP
============================

Powered by Cookiecutter_, Cookiecutter django-SHOP is a framework for jumpstarting a django-SHOP project quickly.

Use this cookiecutter template to run one of the example shops, supplied with django-SHOP.

* Use them to get a first impression on its features.
* Select the example which is the most similar to your own requirements as a blueprint. There replace the
  product models with your own implementations.


Quick How-To
------------

Install cookiecutter_ and npm_ into your global Python site packages, for instance

on Ubuntu

.. code-block:: bash

	sudo apt-get install python-cookiecutter nodejs npm

on MacOS

.. code-block:: bash

	sudo brew install cookiecutter node

then change into your projects directory and invoke

.. code-block:: bash

	cookiecutter --no-input https://github.com/awesto/cookiecutter-django-shop
	cd my-shop
	pipenv install --sequential
	npm install
	export DJANGO_DEBUG=1
	pipenv run ./manage.py runserver


.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _npm: https://www.npmjs.com/get-npm
