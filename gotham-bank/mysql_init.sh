#!/bin/bash

sleep 12

## --user=XXXXXX --password=XXXXXX *may* not be necessary if run as root or you have unsecured DBs but
##   using them makes this script a lot more portable.  Thanks @billkarwin
RESULT=`mysqlshow --user=root --password=very_str0ng_P@ssw0rd  bank -h mysql-whole | grep -v Wildcard | grep -o bank`
if ! [ "$RESULT" ==  "bank" ]; then
    mysql --host=mysql-whole --user=root --password=very_str0ng_P@ssw0rd  < /opt/bank_new.sql
fi


service apache2 start

while :
do
  sleep 1
done





