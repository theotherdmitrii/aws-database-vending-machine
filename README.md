# Database Vending Machine

### Synopsis

The project loads CSV data from s3 bucket into serverless Aurora cluster 

### Prerequisites
1. aws cli v1.17.5+
1. pulumi cli v1.8.1+ 

### How to use

Jump into the project directory with

```bash
$ cd ./pulumi-py-database-vennding-machine/
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

Run `main` script to

```bash
$ ./main
```  

1. create aws stack with serverless Aurora cluster and source s3 bucket 
1. copy data from specified path (by default `./data/dummy.csv`) to newly created s3 bucket
1. run replication task to load CSV files into Aurora cluster

Run `cleanup` to cleanup aws resources 

```bash
$ ./cleanup
```
