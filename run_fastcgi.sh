#!/bin/bash

case "$1" in
"start")
#есть 2 варианта запуска сервера, по сети и через unix сокеты
# последний выигрывает по производительности
su -l rauch -c "python /var/www/gt14.phys.spbu.ru/PyPBS/manage.py runfcgi method=prefork host=127.0.0.1 port=7777 minspare=1 maxspare=1 maxrequests=100 maxchildren=10 pidfile=/tmp/pytorque.pid"

su -l rauch -c "python /var/www/gt14.phys.spbu.ru/PyPBS/manage.py runfcgi method=prefork host=127.0.0.1 port=9001 minspare=1 maxspare=1 maxrequests=100 maxchildren=10 pidfile=/tmp/pytorque_rauch.pid"
su -l www -c "python /var/www/gt14.phys.spbu.ru/PyPBS/manage.py runfcgi method=prefork host=127.0.0.1 port=9002 minspare=1 maxspare=1 maxrequests=100 maxchildren=10 pidfile=/tmp/pytorque_www.pid"
#python ./manage.py runfcgi method=prefork socket=/tmp/sitename.sock pidfile=/tmp/sitename.pid
# не забываем, про то, что сокет у нас мог прочитать фронт-энд
# а nginx  у меня работает с правами www-data
su -l rauch -c "chown rauch:rauch /tmp/pytorque.pid"

su -l rauch -c "chown rauch:rauch /tmp/pytorque_rauch.pid"
su -l www -c "chown www:www /tmp/pytorque_www.pid"
;;
"stop")
su -l rauch -c "kill -9 `cat /tmp/pytorque.pid`"

su -l rauch -c "kill -9 `cat /tmp/pytorque_rauch.pid`"
su -l www -c "kill -9 `cat /tmp/pytorque_www.pid`"
;;
"restart")
$0 stop
sleep 1
$0 start
;;
*) echo "Usage: ./server.sh {start|stop|restart}";;
esac
