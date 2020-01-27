from typing import Any

import boto3
from pulumi.dynamic import Resource, CreateResult, ResourceProvider
from pulumi.output import Output

rds = boto3.client('rds')
snapshot_available_waiter = rds.get_waiter('db_cluster_snapshot_available')


class ClusterSnapshotCopyProps():
    db_cluster_snapshot_identifier: str
    copy_kms_key_arn: str
    name: str

    def __init__(self, name: str, db_cluster_snapshot_identifier: str, copy_kms_key_arn: str):
        self.name = name
        self.db_cluster_snapshot_identifier = db_cluster_snapshot_identifier
        self.copy_kms_key_arn = copy_kms_key_arn


class ClusterSnapshotCopy(Resource):
    arn: Output[str]

    def __init__(self, name, args, opts=None):
        full_args = {'arn': None, **vars(args)}
        super().__init__(ClusterSnapshotCopyProvider(), name, full_args, opts)


class ClusterSnapshotCopyProvider(ResourceProvider):
    def create(self, props: Any):
        copy = rds.copy_db_cluster_snapshot(
            SourceDBClusterSnapshotIdentifier=props['db_cluster_snapshot_identifier'],
            TargetDBClusterSnapshotIdentifier=props['name'],
            KmsKeyId=props['copy_kms_key_arn'])

        copy_arn = copy['DBClusterSnapshot']['DBClusterSnapshotArn']

        snapshot_available_waiter.wait(
            DBClusterSnapshotIdentifier=copy_arn)

        return CreateResult(props["name"], {**props, 'arn': copy_arn})

    def delete(self, _id: str, _props: Any):
        rds.delete_db_cluster_snapshot(
            DBClusterSnapshotIdentifier=_id)
