import pulumi_aws as aws
from pulumi_aws import kms

snapshot_copy_key = kms.Key("key/snapshot_copy_key",
                       is_enabled=True,
                       enable_key_rotation=False)

snapshot_copy_key_alias = aws.kms.Alias("alias/snapshot_copy_key",
                                   target_key_id=snapshot_copy_key.id)

