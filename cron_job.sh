#!/bin/bash

. /etc/profile
. /home/rauch/.profile

cd /home/rauch/PycharmProjects/PyPBS && ./manage.py store_qstat
cd /var/www/gt14.phys.spbu.ru/PyPBS && ./manage.py store_qstat
#export DJANGO_SETTINGS_MODULE=PyPBS.settings
#/home/rauch/PycharmProjects/PyPBS/manage.py store_qstat

#echo "Hello world NEW" > test.txt
