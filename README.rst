cookiecutter-django
=======================

A Cookiecutter_ template for Django.

.. _cookiecutter: https://github.com/audreyr/cookiecutter

Usage
------

First, get cookiecutter::

    $ pip install cookiecutter

Now run it against this repo::

    $ cookiecutter git@git.grimlock.io:mediamoose/cookiecutter-django.git

You'll be prompted for some questions, answer them, then it will create a Django project for you.

**Warning**: repo_name must be a valid Python module name or you will have issues on imports.