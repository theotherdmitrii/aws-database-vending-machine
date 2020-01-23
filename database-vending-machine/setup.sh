#!/usr/bin/env bash

set -e

source ./var.sh

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


echo ---
echo -e started at ${OK}$(date)${NC}
echo started at $(date) > ${SETUP_LOG_FILE}

# Creates KMS copy key
#
echo creating snapshot copy key ...

(cd ./create-snapshot-copy-key/;

# Creates pulumi stack
#
pulumi stack init dev &>> ${SETUP_LOG_FILE};

pulumi up -y &>> ${SETUP_LOG_FILE};

cd - &>/dev/null;)


# Copies snapshot to target account
#
snapshot_copy_key_arn="$(grep -oP 'snapshot_copy_key_arn\s*:\s\"\K([A-Za-z0-9:\-\/_]{30,})' ${SETUP_LOG_FILE})"

echo -e copy key arn ${OK}${snapshot_copy_key_arn}${NC}

snapshot_copy_arn=$(aws rds copy-db-cluster-snapshot \
    --source-db-cluster-snapshot-identifier ${1} \
    --target-db-cluster-snapshot-identifier ${snapshot_name} \
    --kms-key-id ${snapshot_copy_key_arn} \
    --query 'DBClusterSnapshot.DBClusterSnapshotArn' \
    --output text)

echo -e copying source snapshot ${OK}${1}${NC} to ${OK}${snapshot_copy_arn}${NC} ...

echo "snapshot_copy_arn:${snapshot_copy_arn}" >> ${SETUP_LOG_FILE}

echo 'waiting for snapshot copy to complete ...'

aws rds wait db-cluster-snapshot-available \
    --db-cluster-snapshot-identifier ${snapshot_copy_arn}

# Creates Aurora cluster
#
(cd ./create-aurora-cluster/;
echo -e aurora cluster parameters:
echo -e snapshot_copy_key_arn: ${OK}${snapshot_copy_key_arn}${NC}
echo -e snapshot_copy_arn: ${OK}${snapshot_copy_arn}${NC}

echo -e creating aurora cluster ...

# Creates pulumi stack
#
pulumi stack init dev &>> ${SETUP_LOG_FILE};

pulumi config set create-aurora-cluster:snapshot_copy_key_arn ${snapshot_copy_key_arn};

pulumi config set create-aurora-cluster:snapshot_copy_arn ${snapshot_copy_arn};

pulumi config set create-aurora-cluster:master_username ${MASTERUSRENAME};

pulumi config set create-aurora-cluster:master_password ${MASTERPASSWORD};

pulumi up -y &>> ${SETUP_LOG_FILE};

cd - &>/dev/null;)

aurora_cluster_endpoint="$(grep -oP 'aurora_cluster_endpoint\s*:\s\"\K([A-Za-z0-9:\-\/\._]{30,})' ${SETUP_LOG_FILE})"

echo -e Aurora cluster endpoint ${OK}${aurora_cluster_endpoint}${NC}