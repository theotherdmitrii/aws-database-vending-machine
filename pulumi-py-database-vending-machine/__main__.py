import json
import pulumi

from pulumi_aws import dms
from src import s3, database, policies, network, json_util

dms_source_endpoint = dms.Endpoint("nuage-source-s3-endpoint",
                                   endpoint_id="nuage-source-s3-endpoint",
                                   endpoint_type="source",
                                   engine_name="s3",
                                   s3_settings={
                                       "bucket_name": s3.source_bucket.bucket,
                                       "service_access_role_arn": policies.dms_S3_access_role.arn,
                                       "external_table_definition": json_util.escape_json_string(json.dumps({
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
                                   })

dms_target_endpoint = dms.Endpoint("nuage_target_rds_endpoint",
                                   endpoint_id="nuage-target-rds-endpoint",
                                   endpoint_type="target",
                                   engine_name="aurora",
                                   server_name=database.aurora_cluster.endpoint,
                                   username=database.aurora_username,
                                   password=database.aurora_password,
                                   database_name=database.aurora_database,
                                   port=3306)

dms_replication_subnet_group = dms.ReplicationSubnetGroup("nuage_replication_subnetgroup",
                                                          replication_subnet_group_id="nuage-replication-subnetgroup",
                                                          replication_subnet_group_description="Replicaion subnet to populate aurora cluster with the data stored on s3",
                                                          subnet_ids=[
                                                              database.aurora_subnet_0.id,
                                                              database.aurora_subnet_1.id
                                                          ])

dms_replication_instance = dms.ReplicationInstance("nuage_replication_instance",
                                                   replication_instance_id="nuage-replication-instance",
                                                   replication_instance_class="dms.t2.micro",
                                                   replication_subnet_group_id=dms_replication_subnet_group.replication_subnet_group_id,
                                                   # engine_version: "3.1.4",

                                                   vpc_security_group_ids=[
                                                       network.replication_instance_sg.id
                                                   ],
                                                   allocated_storage=20,
                                                   apply_immediately=True,
                                                   publicly_accessible=False)

dms_replication_task = dms.ReplicationTask("nuage_replication_task",
                                           migration_type="full-load",
                                           replication_instance_arn=dms_replication_instance.replication_instance_arn,
                                           replication_task_id="nuage-replication-task",
                                           source_endpoint_arn=dms_source_endpoint.endpoint_arn,
                                           target_endpoint_arn=dms_target_endpoint.endpoint_arn,
                                           table_mappings=json_util.escape_json_string(json.dumps({
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
                                           replication_task_settings=json_util.escape_json_string(json.dumps({
                                               "Logging": {
                                                   "EnableLogging": True,
                                                   "LogComponents": [{
                                                       "Id": "SOURCE_UNLOAD",
                                                       "Severity": "LOGGER_SEVERITY_DEFAULT"
                                                   },{
                                                       "Id": "SOURCE_CAPTURE",
                                                       "Severity": "LOGGER_SEVERITY_DEFAULT"
                                                   },{
                                                       "Id": "TARGET_LOAD",
                                                       "Severity": "LOGGER_SEVERITY_DEFAULT"
                                                   },{
                                                       "Id": "TARGET_APPLY",
                                                       "Severity": "LOGGER_SEVERITY_INFO"
                                                   },{
                                                       "Id": "TASK_MANAGER",
                                                       "Severity": "LOGGER_SEVERITY_DEBUG"
                                                   }]
                                               },
                                           })))



# Exports
pulumi.export('replication_task_arn', dms_replication_task.replication_task_arn)
