db=db.getSiblingDB(process.env.DB_NAME);
//lecteur
db.createUser({
  user: process.env.DB_READ_USER,
  pwd: process.env.DB_READ_PASSWORD,
  roles: [{ role: 'read', db: process.env.DB_NAME }],
});
//editeur
db.createUser({
  user: process.env.DB_READWRITE_USER,
  pwd: process.env.DB_READWRITE_PASSWORD,
  roles: [{ role: 'readWrite', db: process.env.DB_NAME }],
});
//administrateur de la base de données
db.createUser({
  user: process.env.DB_USER,
  pwd: process.env.DB_PASSWORD,
  roles: [{ role: 'dbAdmin', db: process.env.DB_NAME }],
});