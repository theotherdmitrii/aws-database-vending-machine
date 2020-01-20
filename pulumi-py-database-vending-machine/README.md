# Database Vending Machine

### Synopsis

The project loads CSV data from s3 bucket into serverless Aurora cluster 

### Prerequisites
1. aws cli v1.17.5+
1. pulumi v1.8.1+ 

### How to use

Run `./main` script to  

1. create aws stack with serverless Aurora cluster and source s3 bucket 
1. copy data from specified path (by default `./data/dummy.csv`) to newly created s3 bucket
1. run replication task to loda CSV files into Aurora cluster

Run `./cleanup` to cleanup aws resources 
