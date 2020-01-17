import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import * as awsx from "@pulumi/awsx";
import * as random from "@pulumi/random";


// Create a bucket and expose a website index document
const dataBucket = new aws.s3.Bucket("dummydata-bucket", {});

// Construct a VPC
const vpc = new awsx.ec2.Vpc("dummydata_vpc", {
    cidrBlock: "10.0.0.0/16",
});

// Create an Aurora Serverless MySQL database
const auroraSubnet = new aws.rds.SubnetGroup("dummydata_db_subnet", {
    subnetIds: vpc.privateSubnetIds,
});

const auroraMasterPassword = new random.RandomString("password", {
    length: 20,
});

const auroraCluster = new aws.rds.Cluster("dummydata_db", {
    engine: "aurora",
    engineMode: "serverless",
    engineVersion: "5.6.10a",
    dbSubnetGroupName: auroraSubnet.name,
    masterUsername: "pulumi",
    masterPassword: auroraMasterPassword.result,

    // Forces to delete cluster
    skipFinalSnapshot: true
});


function initDatabase(): Promise<any> {
    return new Promise((resolve, reject) => {

        const mysql = require('mysql');

        const connection = mysql.createConnection({
            host: auroraCluster.endpoint.get(),
            user: auroraCluster.masterUsername.get(),
            password: auroraCluster.masterPassword.get(),
            database: auroraCluster.databaseName.get(),
        });


        const s3Path = `s3-${dataBucket.region.get()}://${dataBucket.bucket.get()}/*`;
        console.info(`loading data from s3 path ${s3Path}`);

        connection.connect();
        connection.beginTransaction();

        Promise.all([
            connection.query("DROP DATABASE IF EXISTS dummydata")
        ]).then(
            connection.query("CREATE DATABASE dummydata")
        ).then(
            connection.query("CREATE USER IF NOT EXISTS 'editor'@'0.0.0.0' IDENTIFIED BY 'password'")
        ).then(
            connection.query("GRANT SELECT, INSERT, INDEX ON dummydata.* TO 'editor'@'0.0.0.0'")
        ).then(
            connection.query("GRANT LOAD FROM S3 ON ${s3Path} TO 'editor'@'0.0.0.0'")
        ).then(() => {
            connection.commit();
            console.info("successfully initialized database");
            resolve();

        }).catch(error => {
            connection.rollback();
            console.error(error);
            reject("Fail to initialize database");
        });
    });
}


// Create a Lambda within the VPC to access the Aurora DB and run the code above.
const lambda = new aws.lambda.CallbackFunction("dummydata_db_init_fn", {
    vpcConfig: {
        securityGroupIds: auroraCluster.vpcSecurityGroupIds,
        subnetIds: vpc.privateSubnetIds,
    },
    policies: [
        aws.iam.AWSLambdaVPCAccessExecutionRole,
        aws.iam.AWSLambdaFullAccess,
        aws.iam.AmazonRDSFullAccess
    ],
    callback: async (ev) => {
        console.log(ev);
        await initDatabase();
    },
});

export const functionArn = lambda.arn;

export const databaseEndpoint = auroraCluster.endpoint;
