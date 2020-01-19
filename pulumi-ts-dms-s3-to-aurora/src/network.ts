import * as aws from "@pulumi/aws";
import * as awsx from "@pulumi/awsx";
import * as inputs from "@pulumi/aws/types/input";

export const vpc = new awsx.ec2.Vpc("nuage_vpc", {
    cidrBlock: "10.0.0.0/16",
});

const EgressAll = {
    protocol: "-1", fromPort: 0, toPort: 0, cidrBlocks: ["0.0.0.0/0"]
} as inputs.ec2.SecurityGroupEgress;

export const replicationInstanceSecurityGroup = new aws.ec2.SecurityGroup("nuage_replication_instance_sg", {
    description: "Security group for replication instance",
    egress: [
        EgressAll
    ],
    vpcId: vpc.id
});

export const auroraSecurityGroup = new aws.ec2.SecurityGroup("nuage_db_sg", {
    description: "Security group allows to connect to Aurora cluster from replication SG",
    ingress: [{
        protocol: "tcp", fromPort: 3306, toPort: 3306, securityGroups: [replicationInstanceSecurityGroup.id]
    } as inputs.ec2.SecurityGroupIngress],
    vpcId: vpc.id
});

export const auroraSubnets = vpc.privateSubnetIds;
