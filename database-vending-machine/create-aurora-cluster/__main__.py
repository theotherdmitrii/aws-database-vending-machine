import pulumi
from src.database import aurora_cluster

pulumi.export('aurora_cluster_endpoint', aurora_cluster.endpoint)