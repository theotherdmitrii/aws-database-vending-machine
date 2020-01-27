#!/usr/bin/env bash

set -e

source ./var.sh

SNAPSHOT_ARN_PATTERN='arn:aws:rds:[a-z]{2}-[a-z]+-[0-9]{1}:\d{12}:[A-Za-z0-9\-_]*:\K([A-Za-z0-9:\-_]{4,})'

# validates input
#
if [ "$#" -ne 1  ]; then
    echo -e "${KO}\
Parameters doesn't match, the following expected\n\
\$ deploy.sh <shared_snapshot_arn>${NC}"
    exit 100;
fi

db_cluster_snapshot_arn=${1}
db_cluster_snapshot_copy_name="$(echo ${1} | grep -oP ${SNAPSHOT_ARN_PATTERN})"

if [ -z "$db_cluster_snapshot_copy_name" ]; then
   echo -e "${KO}Invalid snapshot arn ${db_cluster_snapshot_copy_name}${NC}"
   exit 200;
fi

{
    pulumi stack init dev &> /dev/null;
} || echo stack 'dev' already exists

pulumi config set database-vending-machine:db_cluster_snapshot_arn ${db_cluster_snapshot_arn};

pulumi config set database-vending-machine:db_cluster_snapshot_copy_name ${db_cluster_snapshot_copy_name};

pulumi up -y