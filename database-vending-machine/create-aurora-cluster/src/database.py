import pulumi
from pulumi_aws import rds
from .network import aurora_sg, aurora_subnet_0, aurora_subnet_1

aurora_username = "pulumi"
aurora_password = "password"

config = pulumi.Config()

snapshot_copy_key_arn = config.require('snapshot_copy_key_arn')

snapshot_copy_arn = config.require('snapshot_copy_arn')

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
                             # master_username=aurora_username,
                             # master_password=aurora_password,

                             # Forces to delete cluster
                             skip_final_snapshot=True)
