from pulumi_aws import iam

dms_assume_role = iam.get_policy_document(
    statements=[{
        "actions": ["sts:AssumeRole"],
        "principals": [{
            "identifiers": ["dms.amazonaws.com"],
            "type": "Service",
        }],
    }])

dms_S3_access_role = iam.Role("dms-s3-access", assume_role_policy=dms_assume_role.json)

dms_S3_access_role_AmazonS3ReadOnlyAccess = iam.RolePolicyAttachment("dms-s3-access-AmazonS3ReadOnlyAccess",
                                                                     policy_arn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess",
                                                                     role=dms_S3_access_role.name)

dms_cloud_watch_logs_role = iam.Role("dms-cloudwatch-logs-role",
                                     name="dms-cloudwatch-logs-role",
                                     assume_role_policy=dms_assume_role.json)

dms_cloud_watch_logs_role_AmazonDMSCloudWatchLogsRole = iam.RolePolicyAttachment(
    "dms-cloudwatch-logs-role-AmazonDMSCloudWatchLogsRole",
    policy_arn="arn:aws:iam::aws:policy/service-role/AmazonDMSCloudWatchLogsRole",
    role=dms_cloud_watch_logs_role.name)

dms_vpc_role = iam.Role("dms-vpc-role",
                        name="dms-vpc-role",
                        assume_role_policy=dms_assume_role.json)

dms_vpc_role_AmazonDMSVPCManagementRole = iam.RolePolicyAttachment("dms-vpc-role-AmazonDMSVPCManagementRole",
                                                                   policy_arn="arn:aws:iam::aws:policy/service-role/AmazonDMSVPCManagementRole",
                                                                   role=dms_vpc_role.name)
