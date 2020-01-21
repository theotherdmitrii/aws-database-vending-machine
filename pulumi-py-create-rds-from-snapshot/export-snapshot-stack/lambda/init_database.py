import os

import pymysql

queries = [
    f"DROP DATABASE IF EXISTS {schema}",
    f"CREATE DATABASE {schema}",
    f"USE {schema}`",
    f"DROP TABLE IF EXISTS dummydata",
    f"CREATE TABLE dummydata ( id bigint unsigned not null auto_increment, data1 varchar(255) default null, data2 varchar(255) default null, constraint pk_dymmydata primary key (id) )",
    f"INSERT INTO dummydata (id, data1, data2) values (1, \"qwe\", \"asd\")"
]


def handler(event, context):
    endpoint = os.environ["ENDPOINT"]
    database = os.environ["DATABASE"]
    username = os.environ["USERNAME"]
    password = os.environ["PASSWORD"]

    try:
        conn = pymysql.connect(user=username,
                               password=password,
                               host=endpoint,
                               database=database)

        with conn.cursor() as cur:
            for q in queries:
                cur.execute(q)

        conn.commit()

    finally:
        conn.close()

    return "database initialization completed"
