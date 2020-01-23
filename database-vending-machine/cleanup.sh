#!/usr/bin/env bash

# Destroys Aurora cluster stack

BASEDIR=$(pwd)
LOG_FILE="${BASEDIR}/cleanup.log"


# Deletes create-aurora-cluster
#
echo -e destroys Aurora cluster

(cd ./create-aurora-cluster/;

pulumi destroy --skip-preview &>> ${LOG_FILE};

pulumi stack rm dev -y

cd - &>/dev/null;)


# TODO delete kms key


# Deletes create-snapshot-copy-key
#
echo -e destroys snapshot copy key

(cd ./create-snapshot-copy-key/;

pulumi destroy --skip-preview &>> ${LOG_FILE};

pulumi stack rm dev -y

cd - &>/dev/null;)



