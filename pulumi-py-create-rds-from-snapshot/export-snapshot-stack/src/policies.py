import json

from pulumi_aws import iam

# kms_key_policy_document = iam.get_policy_document(
#     statements=[{
#         "principals": [{
#             'arn:aws:iam::104846358986:root',
#         }],
#         "actions": ['kms:*'],
#         "resource": '*'
#     }]
# )

# kms_key_policy = iam.Policy("kms-key-policy", policy=json.dumps({
#     "Version": '2012-10-17',
#     "Id": 'kms-account-access-policy',
#     "Statement": [{
#         "Effect": 'Allow',
#         "Principal": {
#             "AWS": "arn:aws:iam::104846358986:root"
#         },
#         "Action": ['kms:*'],
#         "Resource": '*'
#     }]
# }))

lambda_assume_policy_document = iam.get_policy_document(
    statements=[{
        "actions": ["sts:AssumeRole"],
        "principals": [{
            "identifiers": ["lambda.amazonaws.com"],
            "type": "Service",
        }],
    }])

init_database_role = iam.Role("lambda-rds-access", assume_role_policy=lambda_assume_policy_document.json)

init_database_role_AWSLambdaVPCAccessExecutionRole = iam.RolePolicyAttachment("lambda_access_AmazonS3ReadOnlyAccess",
                                                                              policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole",
                                                                              role=init_database_role.name)

init_database_role_AWSLambdaFullAccess = iam.RolePolicyAttachment("lambda_access_AWSLambdaFullAccess",
                                                                  policy_arn="arn:aws:iam::aws:policy/AWSLambdaFullAccess",
                                                                  role=init_database_role.name)

init_database_role_AmazonRDSFullAccess = iam.RolePolicyAttachment("lambda_access_AmazonRDSFullAccess",
                                                                  policy_arn="arn:aws:iam::aws:policy/AmazonRDSFullAccess",
                                                                  role=init_database_role.name)

init_database_role_AmazonDMSCloudWatchLogsRole = iam.RolePolicyAttachment("lambda_access_AmazonDMSCloudWatchLogsRole",
                                                                          policy_arn="arn:aws:iam::aws:policy/service-role/AmazonDMSCloudWatchLogsRole",
                                                                          role=init_database_role.name)
