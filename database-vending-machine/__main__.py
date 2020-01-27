import pulumi
from src.database import snapshot_copy, aurora_cluster
from src.encryption import snapshot_copy_key

pulumi.export('snapshot_copy_arn', snapshot_copy.arn)
pulumi.export('snapshot_copy_key_arn', snapshot_copy_key.arn)
pulumi.export('aurora_cluster_endpoint', aurora_cluster.endpoint)
