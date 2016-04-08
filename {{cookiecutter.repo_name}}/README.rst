{{ cookiecutter.project_name }}
===============================

{{cookiecutter.description}}


Running in development
----------------------

.. code-block:: console

    docker-compose --project-name {{ cookiecutter.short_name }} --file docker/docker-compose-development.yml up

Or with autoenv

.. code-block:: console

    up

Deployment on {{ cookiecutter.staging_host_name }}
--------------------------------------------------

.. code-block:: console

    docker run -it --rm \
        --net host \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -e DEPLOY_EXECUTABLE=docker/deploy \
        -e PROJECT_NAME={{ cookiecutter.short_name }} \
        -e GIT_REPO={{ cookiecutter.repository }} \
        -e GIT_BRANCH=master \
        -e ENVIRONMENT=staging \
        -e EDIT_ENV=1 \
        mediamoose/deployer:1.0.2


Copyright {% now cookiecutter.timezone, '%Y' %} - License: {{ cookiecutter.open_source_license }}
