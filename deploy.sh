#!/bin/bash

# declare STRING variable
STRING="Deploying Django project yo /var/www/..."
#print variable on a screen
echo $STRING

echo "Removing an old site..."
rm -r /var/www/gt14.phys.spbu.ru/PyPBS

echo "Coping last version to /var/www/..."
cp -r /home/rauch/PycharmProjects/PyPBS /var/www/gt14.phys.spbu.ru/

#echo "Making -ln..."
#cd /var/www/gt14.phys.spbu.ru/PyPBS/media
#ln -s /usr/local/lib/python2.7/dist-packages/django/contrib/admin/media/ admin

echo "Changing rwx rights..."
chown -R rauch:rauch /var/www/gt14.phys.spbu.ru/PyPBS

echo "Allowing everyone's logging"
chmod 666 /var/www/gt14.phys.spbu.ru/PyPBS/logs/pytorque.log 
