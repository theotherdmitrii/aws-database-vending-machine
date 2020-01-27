from pulumi_aws import rds
from .config import db_cluster_snapshot_arn, db_cluster_snapshot_copy_name
from .encryption import snapshot_copy_key
from .network import aurora_sg, aurora_subnet_group
from .database_snapshot import ClusterSnapshotCopy, ClusterSnapshotCopyProps

snapshot_copy = ClusterSnapshotCopy(db_cluster_snapshot_copy_name, ClusterSnapshotCopyProps(
    db_cluster_snapshot_identifier=db_cluster_snapshot_arn,
    copy_kms_key_arn=snapshot_copy_key.arn,
    name='tpch-1gb-shared'))

aurora_cluster = rds.Cluster("nuage_db",
                             engine="aurora",
                             engine_mode="serverless",
                             engine_version="5.6.10a",
                             db_subnet_group_name=aurora_subnet_group.name,
                             vpc_security_group_ids=[
                                 aurora_sg.id
                             ],

                             # Snapshot params
                             snapshot_identifier=snapshot_copy.arn,
                             kms_key_id=snapshot_copy_key.arn,

                             # Overrides master credential for the cluster
                             # master_username=master_username,
                             # master_password=master_password,

                             # Forces to delete cluster
                             skip_final_snapshot=True)
