import * as aws from "@pulumi/aws";

export const dmsAssumeRole = aws.iam.getPolicyDocument({
    statements: [{
        actions: ["sts:AssumeRole"],
        principals: [{
            identifiers: ["dms.amazonaws.com"],
            type: "Service",
        }],
    }],
});

export const dmsS3Access = new aws.iam.Role("dms-s3-access", {
    assumeRolePolicy: dmsAssumeRole.json,
});

const dmsS3Access_AmazonS3ReadOnlyAccess = new aws.iam.RolePolicyAttachment("dms-s3-access-AmazonS3ReadOnlyAccess", {
    //policyArn: "arn:aws:iam::aws:policy/service-role/AmazonS3ReadOnlyAccess",
    policyArn: aws.iam.AmazonS3ReadOnlyAccess,
    role: dmsS3Access.name,
});

const dmsCloudwatchLogsRole = new aws.iam.Role("dms-cloudwatch-logs-role", {
    assumeRolePolicy: dmsAssumeRole.json,
    name: "dms-cloudwatch-logs-role",
});

const dmsCloudwatchLogsRole_AmazonDMSCloudWatchLogsRole = new aws.iam.RolePolicyAttachment("dms-cloudwatch-logs-role-AmazonDMSCloudWatchLogsRole", {
    // policyArn: "arn:aws:iam::aws:policy/service-role/AmazonDMSCloudWatchLogsRole",
    policyArn:aws.iam. AmazonDMSCloudWatchLogsRole,
    role: dmsCloudwatchLogsRole.name,
});

export const dmsVpcRole = new aws.iam.Role("dms-vpc-role", {
    assumeRolePolicy: dmsAssumeRole.json,
    name: "dms-vpc-role",
});

const dmsVpcRole_AmazonDMSVPCManagementRole = new aws.iam.RolePolicyAttachment("dms-vpc-role-AmazonDMSVPCManagementRole", {
    // policyArn: "arn:aws:iam::aws:policy/service-role/AmazonDMSVPCManagementRole",
    policyArn: aws.iam.AmazonDMSVPCManagementRole,
    role: dmsVpcRole.name,
});