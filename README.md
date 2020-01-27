# Database Vending Machine

### Synopsis

The project create serverless Aurora cluster form provided shared cluster snapshot

Please note the program does not create source cluster snapshot.

### Prerequisites
1. Shared snapshot ARN 
1. aws cli v1.17.5+
1. pulumi cli v1.8.1+ 

### How to use

Install Python requirements

```bash
$ virtualenv -p python3 venv
```
```bash
$ source venv/bin/activate
```
```bash
$ pip3 install -r requirements.txt
```


Create new `dev` stack for the program 

```bash
pulumi stack init dev
```

Configure the program

```bash
pulumi config set database-vending-machine:db_cluster_snapshot_arn arn:aws:rds:us-west-1:111111111111:cluster-snapshot:snapshot-shared;

pulumi config set database-vending-machine:db_cluster_snapshot_copy_name snapshot-shared-copy;
```

Run the program

```bash
pulumi up -y
```

OR

Run `deploy.sh` script to create a database copy

```bash
$ ./deploy.sh arn:aws:rds:us-west-1:111111111111:cluster-snapshot:snapshot-shared
```  

Run `destroy.sh` to remove aws resources 

```bash
$ ./destroy.sh
```
