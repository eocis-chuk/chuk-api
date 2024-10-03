#!/bin/bash

# copy relevant files to a remote server

rootfolder=`dirname $0`/..

hostname=$1
username=$2
destfolder=$3

if [ -z ${hostname} ] || [ -z ${username} ] || [ -z ${destfolder} ];
then
  echo provide the hostname, username and destination folder as arguments
else
  rsync -avr --exclude "*/__pycache__" $rootfolder/* $username@$hostname:$destfolder/chuk-api
  rsync -avr $rootfolder/pyproject.toml $username@$hostname:$destfolder/netcdf_explorer
  rsync -avr $rootfolder/setup.cfg $username@$hostname:$destfolder/netcdf_explorer
fi




