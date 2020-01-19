interface QueryParams {
    masterUsername: string,
    masterPassword: string,
    databaseName: string,
    tableName: string,
    importDataPath: string
}

const defaultQueryParams: QueryParams = {
    masterUsername: "",
    masterPassword: "",
    databaseName: "nuage",
    tableName: "dummydata",
    importDataPath: ""
};

export const queries = (params: QueryParams = defaultQueryParams) => {
    const {masterUsername, masterPassword, databaseName, tableName, importDataPath} = params;
    return [
        // creates the database
        `DROP DATABASE IF EXISTS ${databaseName}`,
        `CREATE DATABASE ${databaseName}`,

        // creates Editor user and grants access rights on database and s3
        //`CREATE USER '${editorName}'@'*' IDENTIFIED BY '${editorPassword}'`,
        //`GRANT SELECT, INSERT, UPDATE ON ${databaseName}.* TO '${editorName}'@'%'`,
        //`GRANT SELECT, INSERT, UPDATE ON ${databaseName}.* TO '${editorName}'@'%' IDENTIFIED BY '${editorPassword}'`,

        `GRANT LOAD FROM S3 ON ${databaseName}.* TO '${masterUsername}'@'%'`,
        `FLUSH PRIVILEGES`,

        // create a table
        `USE ${databaseName}`,
        `DROP TABLE IF EXISTS ${tableName}`,
        `CREATE TABLE ${tableName} ( id bigint unsigned not null auto_increment, data1 varchar(255) default null, data2 varchar(255) default null, constraint pk_${tableName} primary key (id) );`,
    ];
};

export interface DatabaseParams {
    host: string,
    masterUsername: string,
    masterPassword: string,
    database: string,
    importDataPath: string
}

export async function initDatabase(params: DatabaseParams): Promise<any> {

    const mysql = require('mysql2/promise');

    const {masterUsername, masterPassword, importDataPath} = params;

    const connection = await mysql.createConnection({
        host: params.host,
        user: params.masterUsername,
        password: params.masterPassword
    });

    const qrys = queries({...defaultQueryParams, masterUsername, masterPassword, importDataPath});

    try {
        await Promise.all(qrys.map(async qry => {
            await connection.beginTransaction();

            try {
                await connection.query(qry);
                await connection.commit();
                console.log(`done ${qry}`)

            } catch (err) {
                await connection.rollback();
                console.error(`error ${qry}\n${err}`);
                throw err
            }
        }));

    } finally {
        connection.destroy()
    }
}

