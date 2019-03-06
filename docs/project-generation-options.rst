Project Generation Options
==========================

project_name:
    Your project's human-readable name, capitals and spaces allowed.

project_slug:
    Your project's slug without dashes or spaces. Used to name your repo
    and in other places where a Python-importable version of your project name
    is needed.

description:
    Describes your project and gets used in places like ``README.rst`` and such.

author_name:
    This is you! The value goes into places like ``LICENSE`` and such.

email:
    The email address you want to identify yourself in the project.

virtual_host:
    The domain name you plan to use for your project once it goes live.
    Note that it can be safely changed later on whenever you need to.

version:
    The version of the project at its inception.

timezone:
    The value to be used for the ``TIME_ZONE`` setting of the project.

use_pycharm:
    Indicates whether the project should be configured for development with PyCharm_.

dockerize:
    Indicates whether the project should be configured to use Docker_ and `Docker Compose`_.
    The choices are:

    1. Do not use Docker.
    2. Use Docker serving HTTP.
    2. Use Docker behind NGiNX serving uwsgi.

use_i18n:
    Indicates whether the project should be configured to use `Django Parler`_,
    supporting more than one language.

use_compressor:
    Indicates whether the project should be configured to use `Django Compressor`_.

debug:
    Indicates whether the project should be configured for debugging.
    This option is relevant for Cookiecutter Django developers only.


.. _PyCharm: https://www.jetbrains.com/pycharm/

.. _Docker: https://github.com/docker/docker
.. _Docker Compose: https://docs.docker.com/compose/

.. _PostgreSQL: https://www.postgresql.org/docs/

.. _Django Compressor: https://github.com/django-compressor/django-compressor
