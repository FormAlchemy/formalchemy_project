#!/bin/sh

make git html
rm -f demo.dat
bin/supervisorctl restart all

