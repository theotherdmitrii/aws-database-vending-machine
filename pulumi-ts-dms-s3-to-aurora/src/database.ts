// Construct a VPC
import * as aws from "@pulumi/aws";

import {auroraSecurityGroup, auroraSubnets} from "./network"

export const auroraUsername = "pulumi";
export const auroraPassword = "password";
export const auroraDatabase = "dummydata";

// Create an Aurora Serverless MySQL database
const auroraSubnetGroup = new aws.rds.SubnetGroup("nuage_db_subnet", {
    subnetIds: auroraSubnets,
});

export const auroraCluster = new aws.rds.Cluster("nuage_db", {
    engine: "aurora",
    engineMode: "serverless",
    engineVersion: "5.6.10a",
    dbSubnetGroupName: auroraSubnetGroup.name,
    masterUsername: auroraUsername,
    masterPassword: auroraPassword,
    databaseName: auroraDatabase,
    vpcSecurityGroupIds: [
        auroraSecurityGroup.id
    ],
    // Forces to delete cluster
    skipFinalSnapshot: true,
});


