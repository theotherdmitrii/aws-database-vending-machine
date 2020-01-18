import {initDatabase} from "./database";

initDatabase({
    host: "localhost",
    masterUsername: "root",
    masterPassword: "password",
    database: "",
    importDataPath: ""
}).then(() =>
    console.info("success")
).catch(err =>
    console.error(err)
);