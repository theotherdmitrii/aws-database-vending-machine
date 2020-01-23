# Database Vending Machine

### Synopsis

The project restores shared snapshot into serverless Aurora cluster 

### Prerequisites
1. aws cli v1.17.5+
1. pulumi cli v1.8.1+ 

### How to use

Jump into the project directory with

```bash
$ cd ./database-vennding-machine/
```

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

Run `setup.sh` script to

```bash
$ ./setup.sh arn:aws:rds:us-west-1:111111111111:cluster-snapshot:snapshot-shared
```  

1. create kms key to encrypt a copy of a shared cluster snapshot
1. copy shared cluster snapshot into current account
1. create serverless Aurora cluster form copied snapshot

Run `cleanup.sh` to cleanup aws resources 

```bash
$ ./cleanup.sh
```
