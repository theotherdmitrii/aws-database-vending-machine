#!/usr/bin/env bash

# color scheme
export OK='\033[0;34m'
export KO='\033[0;31m'
export NC='\033[0m'

BASEDIR=$(pwd)

export SETUP_LOG_FILE="${BASEDIR}/setup.log"

export CLEANUP_LOG_FILE="${BASEDIR}/cleanup.log"

export MASTERUSRENAME="nuage"

export MASTERPASSWORD="passw0rd"
