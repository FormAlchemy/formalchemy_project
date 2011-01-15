#!/bin/sh

cd $(dirname $0)

make $@
rm -f demo.dat
bin/supervisorctl restart all

