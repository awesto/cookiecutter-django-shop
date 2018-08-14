Cookiecutter for django-SHOP
============================

Powered by Cookiecutter_, **cookiecutter-django-shop** is a set of templates for jumpstarting a django-SHOP project
quickly.

Use this Cookiecutter to run one of the example shops, supplied with django-SHOP.

* Use them to get a first impression on its features.
* Select the example which is the most similar to your own requirements as a blueprint. There replace the
  product models with your own implementations.


Quick How-To
------------

Install cookiecutter_ and npm_ onto your operating system, for instance

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
	pipenv run ./manage.py makemigrations myshop
	pipenv run ./manage.py initialize_shop_demo
	pipenv run ./manage.py runserver


Where to proceed from here?
---------------------------

Now that you have a simple working project, it usually is much easier to evolve into a real project for the merchant's
needs. Remember that there are 6 different demos and depending on the requirements, use one of them as a blueprint.

Rerun the above ``cookiecutter`` command without the ``--no-input`` flag and answer the questions. Use the generated
Django models as blueprint, rename them and replace their fields to whatever is approriate to the shop's specifications.


.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _npm: https://www.npmjs.com/get-npm
