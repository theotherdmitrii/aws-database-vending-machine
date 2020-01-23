#!/usr/bin/env bash

source ./var.sh

# Deletes snapshot
#
snapshot_copy_arn="$(grep -oP 'snapshot_copy_arn\s*:\s*\"\K([A-Za-z0-9:\-\/_]{30,})' ${SETUP_LOG_FILE})"

echo ${snapshot_copy_arn}

if [ ! -z "$snapshot_copy_arn" ]; then
{
    echo -e Deleting snapshot ${OK}${snapshot_copy_arn}${NC}

    aws rds delete-db-cluster-snapshot \
        --db-cluster-snapshot-identifier ${snapshot_copy_arn} &>/dev/null;

    echo -e ensuring snapshot copy ${OK}${snapshot_copy_arn}${NC} has been deleted

    aws rds wait db-cluster-snapshot-deleted \
        --db-cluster-snapshot-identifier ${snapshot_copy_arn} &>/dev/null;

} || echo -e snaphsot ${OK}${snapshot_copy_arn}${NC} not found
fi

#{
#    # Destroys Aurora cluster stack
#    #
#    echo -e destroys Aurora cluster
#
#    cd ./create-aurora-cluster/;
#
#    pulumi destroy --skip-preview &>> ${CLEANUP_LOG_FILE};
#
#    pulumi stack rm dev -y &>/dev/null;
#
#    cd - &>/dev/null;
#
#} || echo -e aurora cluster not found
#
#
#{
#    # Deletes create-snapshot-copy-key
#    #
#    echo -e destroys snapshot copy key
#
#    cd ./create-snapshot-copy-key/;
#
#    pulumi destroy --skip-preview &>> ${CLEANUP_LOG_FILE};
#
#    pulumi stack rm dev -y &>/dev/null;
#
#    cd - &>/dev/null;
#
#} || echo -e snapshot copy key not found