#!/usr/bin/env bash

set -e

# color scheme
OK='\033[0;34m'
KO='\033[0;31m'
NC='\033[0m'

# constants
#
BASEDIR=$(pwd)

LOG_FILE="${BASEDIR}/setup.log"

SNAPSHOT_ARN_PATTERN='arn:aws:rds:[a-z]{2}-[a-z]+-[0-9]{1}:\d{12}:[A-Za-z0-9\-_]*:\K([A-Za-z0-9:\-_]{4,})'


# validates input
#
if [ "$#" -ne 1  ]; then
    echo -e "${KO}\
Parameters doesn't match, the following expected\n\
\$ copy-shared-snapshot <shared_snapshot_arn>${NC}"
    exit 100;
fi

snapshot_name="$(echo ${1} | grep -oP ${SNAPSHOT_ARN_PATTERN})"

if [ -z "$snapshot_name" ]; then
   echo -e "${KO}Invalid snapshot arn ${snapshot_name}${NC}"
   exit 200;
fi


if [ -z "$AWS_DEFAULT_REGION" ]; then
   echo -e "${KO}Environment valiable AWS_DEFAULT_REGION not set${NC}"
   exit 300;
fi


echo started at $(date)
echo started at $(date) > ${LOG_FILE}

# Creates pulumi stack
#
pulumi stack init dev &>> ${LOG_FILE};


# Creates KMS copy key
#
echo creating snapshot copy key ...

(cd ./create-snapshot-copy-key/; pulumi up -y &>> ${LOG_FILE}; cd -;)

# Copies snapshot to target account
#
snapshot_copy_key_arn="$(grep -oP 'snapshot_copy_key_arn\s*:\s\"\K([A-Za-z0-9:\-\/_]{30,})' ${LOG_FILE})"

echo -e copy key arn ${OK}${snapshot_copy_key_arn}${NC}

echo -e copying source snapshot ${OK}${1}${NC} to region ${OK}${AWS_DEFAULT_REGION}${NC} as ${OK}${snapshot_name}${NC} ...

snapshot_copy_arn=$(aws rds copy-db-cluster-snapshot \
    --source-db-cluster-snapshot-identifier ${1} \
    --target-db-cluster-snapshot-identifier ${snapshot_name} \
    --kms-key-id ${snapshot_copy_key_arn} \
    --query 'DBClusterSnapshot.DBClusterSnapshotArn' \
    --output text)

snapshot_copy_arn="arn:aws:rds:eu-west-1:126563215282:cluster-snapshot:tpch-1gb-shared"


# Creates Aurora cluster
#
echo -e snapshot copy arn ${OK}${snapshot_copy_arn}${NC}

(cd ./create-aurora-cluster/;
echo -e "-- Aurora cluster parameters:"
echo -e snapshot_copy_key_arn: ${OK}${snapshot_copy_key_arn}${NC}
echo -e snapshot_copy_arn: ${OK}${snapshot_copy_arn}${NC}

echo -e creating Aurora cluster ...

pulumi config set snapshot_copy_key_arn ${snapshot_copy_key_arn};

pulumi config set snapshot_copy_arn ${snapshot_copy_arn};

pulumi up -y &>> ${LOG_FILE};

cd -;)

aurora_cluster_endpoint="$(grep -oP 'aurora_cluster_endpoint\s*:\s\"\K([A-Za-z0-9:\-\/\._]{30,})' ${LOG_FILE})"

echo Aurora cluster endpoint ${aurora_cluster_endpoint}