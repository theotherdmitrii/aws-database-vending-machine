import pulumi

config = pulumi.Config()

snapshot_copy_key_arn = config.require('snapshot_copy_key_arn')

snapshot_copy_arn = config.require('snapshot_copy_arn')

master_username = config.require('master_username')

master_password = config.require('master_password')