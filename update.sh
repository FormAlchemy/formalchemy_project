#!/bin/sh

make $@
rm -f demo.dat
bin/supervisorctl restart all

