#!/bin/bash
set -e
[ $DEBUG ] && set -x

source /env-vars.sh
source /functions.sh

$@

exit 0
