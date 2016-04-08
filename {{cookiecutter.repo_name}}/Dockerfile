FROM mediamoose/python34:1.2.0

MAINTAINER {{ cookiecutter.author_name }} <{{ cookiecutter.author_email }}>

ENV DJANGO_SETTINGS_MODULE=main.settings.production

EXPOSE 9000 9191
WORKDIR /project

COPY requirements.txt /project/
COPY requirements_dev.txt /project/
COPY requirements_test.txt /project/
RUN pip install --requirement requirements.txt \
 && export PYTHONUSERBASE=/project/env/testing && pip install --user --requirement requirements_test.txt \
 && export PYTHONUSERBASE=/project/env/development && pip install --user --requirement requirements_dev.txt

COPY docker/django/manage /usr/local/bin/
COPY docker/django/env-vars.sh /
COPY docker/django/functions.sh /
COPY docker/django/entrypoint.sh /
COPY docker/django/uwsgi.ini /etc/uwsgi/

COPY .isort.cfg /project/
COPY .coveragerc /project/

COPY src /project/src

ENTRYPOINT ["/entrypoint.sh"]
CMD ["python"]
