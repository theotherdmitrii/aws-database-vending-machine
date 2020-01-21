import pulumi_aws as aws
from pulumi_aws import ec2

EgressAll = {
    "protocol": "-1", "from_port": 0, "to_port": 0, "cidr_blocks": ["0.0.0.0/0"]
}

azs = aws.get_availability_zones(state="available")

azIds = azs.zone_ids

vpc = ec2.Vpc("nuage_vpc", cidr_block="10.0.0.0/16")


aurora_sg = ec2.SecurityGroup("nuage_db_sg",
                              description="Security group allows to connect to Aurora cluster from replication SG",
                              ingress=[
                              # No ingress rules yet
                              ],
                              vpc_id=vpc.id
                              )

aurora_subnet_0 = ec2.Subnet(f"{vpc._name}-private-0",
                             cidr_block="10.0.0.0/24",
                             availability_zone_id=azIds[0],
                             vpc_id=vpc.id)

aurora_subnet_1 = ec2.Subnet(f"{vpc._name}-private-1",
                             cidr_block="10.0.4.0/24",
                             availability_zone_id=azIds[1],
                             vpc_id=vpc.id)

aurora_subnet_ids = [aurora_subnet_0.id, aurora_subnet_1.id]