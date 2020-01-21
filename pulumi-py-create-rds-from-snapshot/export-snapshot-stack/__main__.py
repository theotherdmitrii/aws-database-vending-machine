import pulumi

from src.function import *
from src.database import *
from src.encryption import *



pulumi.export('function.arn', init_database_fn.arn)
pulumi.export('database.endpoint', aurora_cluster.endpoint)
pulumi.export('kms.key.alias', snapshot_key_alias.name)