import pulumi

from .database import *
from .network import *
from .policies import *
from  .encryption import *

init_database_fn = aws.lambda_.Function('init_database_fn',
                                        vpc_config={
                                            "security_group_ids": aurora_cluster.vpc_security_group_ids,
                                            "subnet_ids": aurora_subnet_ids
                                        },
                                        role=init_database_role.arn,
                                        runtime="python3.7",
                                        handler="init_database.handler",
                                        code=pulumi.AssetArchive({
                                            '.': pulumi.FileArchive('./lambda')
                                        }),
                                        environment={
                                            "variables": {
                                                "ENDPOINT": aurora_cluster.endpoint,
                                                "DATANASE": aurora_database,
                                                "USERNAME": aurora_username,
                                                "PASSWORD": aurora_password
                                            }
                                        })
