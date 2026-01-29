db = db.getSiblingDB("healthcare_db");

db.createUser({
  user: "read_user",
  pwd: "read_password",
  roles: [{ role: "read", db: "healthcare_db" }],
});

db.createUser({
  user: "readwrite_user",
  pwd: "readwrite_password",
  roles: [{ role: "readWrite", db: "healthcare_db" }],
});

db.createUser({
  user: "admin_user",
  pwd: "admin_password",
  roles: [{ role: "dbAdmin", db: "healthcare_db" }],
});
