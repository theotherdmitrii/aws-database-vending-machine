import * as aws from "@pulumi/aws";
import {auroraCluster, auroraDatabase, auroraPassword, auroraUsername} from "./src/database";
import {auroraSubnets, replicationInstanceSecurityGroup} from "./src/network";
import {sourceBucket} from "./src/s3";
import {dmsS3Access} from "./src/policies";


const dmsSourceEndpoint = new aws.dms.Endpoint("nuage-source-s3-endpoint", {
    endpointId: "nuage-source-s3-endpoint",
    endpointType: "source",
    engineName: "s3",
    s3Settings: {
        bucketName: sourceBucket.bucket,
        serviceAccessRoleArn: dmsS3Access.arn,
        externalTableDefinition: escapeJSONString(JSON.stringify({
            "TableCount": "1",
            "Tables": [
                {
                    "TableName": "dummydata",
                    "TablePath": "root/dummydata/",
                    "TableOwner": "root",
                    "TableColumns": [
                        {
                            "ColumnName": "id",
                            "ColumnType": "INT8",
                            "ColumnNullable": "false",
                            "ColumnIsPk": "true"
                        },
                        {
                            "ColumnName": "data1",
                            "ColumnType": "STRING",
                            "ColumnLength": "255"
                        },
                        {
                            "ColumnName": "data2",
                            "ColumnType": "STRING",
                            "ColumnLength": "255"
                        }
                    ],
                    "TableColumnsTotal": "3"
                }
            ]
        })),
    }
});

const dmsTargetEndpoint = new aws.dms.Endpoint("nuage_target_rds_endpoint", {
    endpointId: "nuage-target-rds-endpoint",
    endpointType: "target",
    engineName: "aurora",
    serverName: auroraCluster.endpoint,
    username: auroraUsername,
    password: auroraPassword,
    databaseName: auroraDatabase,
    port: 3306,
});

const dmsReplicationSubnetGroup = new aws.dms.ReplicationSubnetGroup("nuage_replication_subnetgroup", {
    replicationSubnetGroupId: "nuage-replication-subnetgroup",
    replicationSubnetGroupDescription: "Replicaion subnet to populate aurora cluster with the data stored on s3",
    subnetIds: auroraSubnets
});

// Create a new replication instance
const dmsReplicationInstance = new aws.dms.ReplicationInstance("nuage_replication_instance", {
    replicationInstanceId: "nuage-replication-instance",
    replicationInstanceClass: "dms.t2.micro",
    replicationSubnetGroupId: dmsReplicationSubnetGroup.replicationSubnetGroupId,
    // engineVersion: "3.1.4",

    vpcSecurityGroupIds: [
        replicationInstanceSecurityGroup.id
    ],
    allocatedStorage: 20,
    applyImmediately: true,
    publiclyAccessible: false
});

const dmsReplicationTask = new aws.dms.ReplicationTask("nuage_replication_task", {
    migrationType: "full-load",
    replicationInstanceArn: dmsReplicationInstance.replicationInstanceArn,
    replicationTaskId: "nuage-replication-task",
    sourceEndpointArn: dmsSourceEndpoint.endpointArn,
    targetEndpointArn: dmsTargetEndpoint.endpointArn,
    tableMappings: escapeJSONString(JSON.stringify({
        "rules": [
            {
                "rule-type": "selection",
                "rule-id": "1",
                "rule-name": "1",
                "object-locator": {
                    "schema-name": "%",
                    "table-name": "%"
                },
                "rule-action": "include"
            }
        ]
    })),
});

function escapeJSONString(json: string) {
    return json.replace(/\\n/g, "\\n")
        .replace(/\\'/g, "\\'")
        .replace(/\\"/g, '\\"')
        .replace(/\\&/g, "\\&")
        .replace(/\\r/g, "\\r")
        .replace(/\\t/g, "\\t")
        .replace(/\\b/g, "\\b")
        .replace(/\\f/g, "\\f");
}