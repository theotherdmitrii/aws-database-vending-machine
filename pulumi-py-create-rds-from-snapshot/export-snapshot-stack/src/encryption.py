import pulumi_aws as aws
from pulumi_aws import kms
from .policies import *

snapshot_key = kms.Key("snapshot_key",
                       is_enabled=True,
                       enable_key_rotation=False,
                       policy=json.dumps({
                           "Version": '2012-10-17',
                           "Id": 'kms-account-access-policy',
                           "Statement": [{
                               "Effect": 'Allow',
                               "Principal": {
                                   "AWS": "arn:aws:iam::104846358986:root"
                               },
                               "Action": ['kms:*'],
                               "Resource": '*'
                           }]
                       }))

snapshot_key_alias = aws.kms.Alias("alias/snapshot_key",
                                   target_key_id=snapshot_key.id)

