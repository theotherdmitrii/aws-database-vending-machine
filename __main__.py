import pulumi_random as random
from pulumi_aws import ec2, iam, rds, s3
import json

# Params
vpc_name = "nuage-vpc"
csv_bucket_pref = "nuage"
csv_bucket_suf = random.RandomString("target-bucket-prefix", length=8)
db_master_useranme = "nuage"
db_master_password = random.RandomString("password", length=20)


# Creates an AWS data bucket to hold CSV
csv_bucket = s3.Bucket(f'{csv_bucket_pref}-{csv_bucket_suf}')

# Creates IAM roles to load CSV from s3
rds_role = iam.Role('RdsReadS3Role',
                    assume_role_policy=json.dumps({
                        "Version": "2012-10-17",
                        "Statement": [{
                            "Action": "sts:AssumeRole",
                            "Principal": {
                                "Service": "rds.amazonaws.com"
                            },
                            "Effect": "Allow",
                            "Sid": ""
                        }]
                    }))

rds_role_policy = iam.RolePolicy('RdsReadS3RolePolicy',
                                 role=rds_role.id,
                                 policy=json.dumps({
                                     "Version": "2012-10-17",
                                     "Statement": [{
                                         "Effect": "Allow",
                                         "Action": [
                                             "s3:ListBucket",
                                             "s3:GetObject",
                                             "s3:GetObjectVersion",
                                         ],
                                         "Resource": [
                                             f"{csv_bucket.arn}",
                                             f"{csv_bucket.arn}/*"
                                         ]
                                     }]
                                 }))



# Creates VPC and Subnet Group for the cluster
# vpc = ec2.Vpc(vpc_name,
#               cidr_block="10.0.0.0/16")
# db_subnet = rds.SubnetGroup()

# Creates VPC endpoint to allow assess RDS to s3 data bucket
# TODO

# Creates Database cluster
database = rds.Cluster("database",
                       engine="aurora",
                       engine_mode="serverless",
                       engine_version="5.6.10a",
                       master_username=db_master_useranme,
                       master_password=db_master_password,
                       # WARN! DOESN'T CREATE A SNAPSHOT ON DESTROY
                       skip_final_snapshot=True)

# Configure init SQL script for the cluster to load CSV data from the bucket

# Exports
# pulumi.export('bucket_name', target_bucket.id)
