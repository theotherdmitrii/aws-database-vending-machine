import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import * as awsx from "@pulumi/awsx";
import * as random from "@pulumi/random";
import {initDatabase} from "./src/database"

// Create a bucket and expose a website index document
const dataBucket = new aws.s3.Bucket("nuage_bucket", {});

// Construct a VPC
const vpc = new awsx.ec2.Vpc("nuage_vpc", {
    cidrBlock: "10.0.0.0/16",
});

const auroraSubnets = vpc.privateSubnetIds;

// Create an Aurora Serverless MySQL database
const auroraSubnet = new aws.rds.SubnetGroup("nuagedb_subnet", {
    subnetIds: auroraSubnets,
});

const auroraMasterPassword = new random.RandomString("password", {
    length: 20,
});

const auroraCluster = new aws.rds.Cluster("nuage_db", {
    engine: "aurora",
    engineMode: "serverless",
    engineVersion: "5.6.10a",
    dbSubnetGroupName: auroraSubnet.name,
    masterUsername: "pulumi",
    masterPassword: auroraMasterPassword.result,
    iamRoles: [
        // auroraS3ReadRole.arn
        aws.iam.AmazonS3ReadOnlyAccess
    ],
    // Forces to delete cluster
    skipFinalSnapshot: true,
});

// Create a Lambda within the VPC to access the Aurora DB and run the code above.
const databaseInitFun = new aws.lambda.CallbackFunction("nuage_db_init_fn", {
    vpcConfig: {
        securityGroupIds: auroraCluster.vpcSecurityGroupIds,
        subnetIds: auroraSubnets,
    },
    policies: [
        aws.iam.AWSLambdaVPCAccessExecutionRole,
        aws.iam.AWSLambdaFullAccess,
        aws.iam.AmazonRDSFullAccess
    ],
    callback: async (ev) => {
        console.log(ev);

        const dymmydataS3Path = `s3-${dataBucket.region.get()}://${dataBucket.bucket.get()}/*`;

        console.info(`loading data from s3 path ${dymmydataS3Path}`);

        await initDatabase({
            host: auroraCluster.endpoint.get(),
            masterUsername: auroraCluster.masterUsername.get(),
            masterPassword: auroraCluster.masterPassword.get()!!,
            database: auroraCluster.databaseName.get(),
            importDataPath: dymmydataS3Path
        });
    },
});

export const functionArn = databaseInitFun.arn;