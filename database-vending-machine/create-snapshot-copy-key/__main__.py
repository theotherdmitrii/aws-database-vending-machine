import pulumi
from src.encryption import *

pulumi.export('snapshot_copy_key_arn', snapshot_copy_key.arn)