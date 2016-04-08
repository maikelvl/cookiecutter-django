#!/bin/sh

start_uwsgi() {
    manage collectstatic --no-input
    _wait_for_database
    _wait_for_elasticsearch
    _prepare_media
    echo 'Starting uwsgi...'
    uwsgi /etc/uwsgi/uwsgi.ini
}

manage() {
    python src/manage.py $@
}

runserver() {
    options=$@
    if [ ! $options ];then
        options="0.0.0.0:9000"
    fi
    _prepare_media
    _wait_for_database
    _wait_for_elasticsearch
    exec python /project/src/manage.py runserver $options
}

pip_outdated_env() {
	echo "Outdated $2:"
	unset PYTHONUSERBASE
	if [ "$1" != "base" ];then
 		export PYTHONUSERBASE=/project/env/$1
 		pip_args="--user"
	fi
	export PYTHONUSERBASE=/project/env/$1
	while read line;do
		echo "  - $line"
	done < <(pip list $pip_args --outdated)
	unset PYTHONUSERBASE
	echo ''
}

pip_outdated() {
	pip_outdated_env base requirement.txt $@
	pip_outdated_env testing requirements_test.txt $@
	pip_outdated_env development requirements_dev.txt $@}
}

pip_update_env() {
	echo "Updating $2:"
	unset PYTHONUSERBASE
	if [ "$1" != "base" ];then
 		export PYTHONUSERBASE=/project/env/$1
 		pip_args="--user"
	fi
	pip install $pip_args --upgrade --requirement $1
	if [ "$3" == "--save" ];then
		pip_freeze_env $@
	fi
	echo ''
	unset PYTHONUSERBASE
}

pip_update() {
	pip_update_env base requirement.txt $@
	pip_update_env testing requirements_test.txt $@
	pip_update_env development requirements_dev.txt $@
}

pip_freeze_env() {
	echo "Freezing $2:"
	unset PYTHONUSERBASE
	if [ "$1" != "base" ];then
 		export PYTHONUSERBASE=/project/env/$1
 		pip_args="--user"
	fi
	freeze="$(pip freeze $pip_args)"
	rm $2.freeze
	while read line;do
		package="$(echo "$line" | sed -rn "s/([^=\<\>]+).*/\1/p")"
		if [ "$package" != "$line" ];then
			package="$(echo "$freeze" | grep -ie "^${package}==.*$")"
		fi
		echo "$package" >> $2.freeze
	done < $2
	unset PYTHONUSERBASE
}

pip_freeze() {
	pip_freeze_env base requirement.txt $@
	pip_freeze_env testing requirements_test.txt $@
	pip_freeze_env development requirements_dev.txt $@
}

version() {
    uwsgi --version
}

_wait_for_database() {
    if [ "$DJANGO_DATABASE_HOST" == "" ] || [ "$DJANGO_DATABASE_PORT" == "" ];then
        return 0
    fi
    echo "Waiting for database ($DJANGO_DATABASE_HOST:$DJANGO_DATABASE_PORT)..."
    while true;do
        if nc -zw3 $DJANGO_DATABASE_HOST $DJANGO_DATABASE_PORT;then
            break
        fi
        echo -n '.'
        sleep 1
    done
    echo ''
    if [ $DJANGO_MIGRATE ];then
        manage migrate --noinput
    fi
}

_wait_for_elasticsearch() {
    if [ "$DJANGO_ELASTICSEARCH_HOST" == "" ] || [ "$DJANGO_ELASTICSEARCH_PORT" == "" ];then
        return 0
    fi
    echo "Waiting for ELASTICSEARCH ($DJANGO_ELASTICSEARCH_HOST:$DJANGO_ELASTICSEARCH_PORT)..."
    while true;do
        if nc -zw3 $DJANGO_ELASTICSEARCH_HOST $DJANGO_ELASTICSEARCH_PORT;then
            break
        fi
        echo -n '.'
        sleep 1
    done
    echo ''
    if [ $DJANGO_REBUILD_SEARCH_INDEX ];then
        manage rebuild_index --noinput
    fi
}

_prepare_media() {
    mkdir -p $MEDIA_PATH
    chmod 777 -R $MEDIA_PATH
}

test_exit() {
    coverage erase
}

test() {
    trap test_exit SIGINT EXIT
    isort --check-only -q -rc /project/src/$1
    flake8 --exclude=*/__init__.py,src/main/settings/*.py,*/migrations/* /project/src/$1
    coverage run --branch -a --source=/project/src/$1 /project/src/manage.py collectstatic --no-input --settings=main.settings.testing
    _wait_for_database
    _wait_for_elasticsearch
    coverage run --branch -a --source=/project/src/$1 -m py.test /project/src/$1 --ds=main.settings.testing
    coverage report -m --skip-covered
    coverage html
    coverage xml
    test_exit
}

pytest() {
    if [ $1 ];then
        test_path="/$1"
        shift
    fi
    py.test /project/src${test_path} --ds=main.settings.testing $@
}
