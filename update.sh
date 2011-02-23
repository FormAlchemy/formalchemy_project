#!/bin/sh

cd $(dirname $0)

rm -f demo.db
bin/supervisorctl restart all

