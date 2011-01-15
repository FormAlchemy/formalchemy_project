#!/bin/sh

cd $(dirname $0)

rm -f demo.dat
bin/supervisorctl restart all

