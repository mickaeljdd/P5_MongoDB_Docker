const dbName = process.env.MONGO_INITDB_DATABASE || "healthcare_db";
const readUser = process.env.DB_READ_USER || "read_user";
const readPassword = process.env.DB_READ_PASSWORD || "read_password";
const readWriteUser = process.env.DB_READWRITE_USER || "readwrite_user";
const readWritePassword = process.env.DB_READWRITE_PASSWORD || "readwrite_password";

db = db.getSiblingDB(dbName);

db.createUser({
  user: readUser,
  pwd: readPassword,
  roles: [{ role: "read", db: dbName }],
});

db.createUser({
  user: readWriteUser,
  pwd: readWritePassword,
  roles: [{ role: "readWrite", db: dbName }],
});
