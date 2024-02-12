#!/bin/bash

# copy relevant files to JASMIN

rootfolder=`dirname $0`/..
username=$1
destfolder=$2

if [ -z ${username} ] || [ -z ${destfolder} ];
then
  echo provide the username and destination folder on JASMIN as arguments
else
  rsync -avr --delete --exclude "*/__pycache__" $rootfolder/* $username@login2.jasmin.ac.uk:$destfolder/chuk-api
fi




