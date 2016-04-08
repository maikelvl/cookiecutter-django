#!/bin/bash
set -e
[ $DEBUG ] && set -x

echo "$TIMEZONE" > /etc/timezone && dpkg-reconfigure -f noninteractive tzdata

install() {
    npm install --unsafe-perm
    bower install --allow-root --config.interactive=false
    build
}

build() {
    grunt build
}

watch() {
    build
    while true;do
        grunt
    done
}

$@
exit 0
