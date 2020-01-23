from pulumi_aws import rds

from .config import snapshot_copy_key_arn, snapshot_copy_arn, master_username, master_password
from .network import aurora_sg, aurora_subnet_0, aurora_subnet_1

aurora_subnet_group = rds.SubnetGroup("nuage_db_subnet",
                                      subnet_ids=[
                                          aurora_subnet_0.id,
                                          aurora_subnet_1.id
                                      ])

aurora_cluster = rds.Cluster("nuage_db",
                             engine="aurora",
                             engine_mode="serverless",
                             engine_version="5.6.10a",
                             db_subnet_group_name=aurora_subnet_group.name,
                             vpc_security_group_ids=[
                                 aurora_sg.id
                             ],

                             # Snapshot params
                             snapshot_identifier=snapshot_copy_arn,
                             kms_key_id=snapshot_copy_key_arn,

                             # Overrides master credential for the cluster
                             master_username=master_username,
                             master_password=master_password,

                             # Forces to delete cluster
                             skip_final_snapshot=True)
