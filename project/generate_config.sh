#!/bin/bash

CONFIG="config.ini"

rm -f $CONFIG

echo [DATABASE] >> $CONFIG
echo host = 127.0.0.1 >> $CONFIG
echo user = postgres >> $CONFIG
echo database = postgres >> $CONFIG
echo password = tingle12345 >> $CONFIG
echo secret_key = /TMVe0Lwhc*0I >> $CONFIG

echo [EMAIL] >> $CONFIG
echo base_url = abc.com >> $CONFIG
echo email = example@example.com >> $CONFIG
echo email_password = 12345678 >> $CONFIG