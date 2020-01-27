import pulumi

config = pulumi.Config()

db_cluster_snapshot_arn = config.require('db_cluster_snapshot_arn')

db_cluster_snapshot_copy_name = config.require('db_cluster_snapshot_copy_name')