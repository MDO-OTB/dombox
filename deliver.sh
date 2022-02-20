#!/bin/sh
tar  -chvf dombox.tar -C target .
scp dombox.tar     root@$1:/root/
