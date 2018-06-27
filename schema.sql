DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS permission;
DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS role_permission;
DROP TABLE IF EXISTS user_role;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_name TEXT UNIQUE NOT NULL,
  full_name TEXT NOT NULL,
  password TEXT NOT NULL,
  enabled INTEGER DEFAULT 1
);

CREATE TABLE permission (
  id INTEGER PRIMARY KEY,
  permission_name TEXT UNIQUE NOT NULL
);

CREATE TABLE role (
  id INTEGER PRIMARY KEY,
  role_name TEXT UNIQUE NOT NULL
);

CREATE TABLE role_permission (
  role_id INTEGER NOT NULL,
  permission_id INTEGER NOT NULL,
  FOREIGN KEY (role_id) REFERENCES role (id),
  FOREIGN KEY (permission_id) REFERENCES permission (id),
  PRIMARY KEY (role_id, permission_id)
);

CREATE TABLE user_role (
  user_id INTEGER NOT NULL,
  role_id INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user (id),
  FOREIGN KEY (role_id) REFERENCES role (id),
  PRIMARY KEY (user_id, role_id)
);

INSERT INTO user (id, user_name, full_name, password) VALUES
(0, "admin", "Administrator", "admin"),
(1, "data", "Data Operator", "data"),
(2, "qa", "Validation Engineer", "qa");

INSERT INTO permission(id, permission_name) VALUES
(0, "ADMIN"),
(1, "DRAFT"),
(2, "SUBMITTED"),
(3, "APPROVED"),
(4, "REJECTED"),
(5, "REVOKED"),
(6, "EDIT_DRAFT"),
(7, "EDIT_SUBMITTED"),
(8, "EDIT_APPROVED"),
(9, "EDIT_REJECTED"),
(10, "EDIT_REVOKED"),
(11, "DELETE_DRAFT"),
(12, "DELETE_SUBMITTED"),
(13, "DELETE_APPROVED"),
(14, "DELETE_REJECTED"),
(15, "DELETE_REVOKED"),
(16, "CREATE"),
(17, "SUBMIT"),
(18, "APPROVE"),
(19, "REJECT"),
(20, "REVOKE");

INSERT INTO role(id, role_name) VALUES
(0, "ADMINISTRATOR"),
(1, "DATA_ENTRY"),
(2, "DATA_VALIDATION");

INSERT INTO role_permission(role_id, permission_id) VALUES
(0, 0),
(0, 1),
(0, 2),
(0, 3),
(0, 4),
(0, 5),
(0, 6),
(0, 7),
(0, 8),
(0, 9),
(0, 10),
(0, 11),
(0, 12),
(0, 13),
(0, 14),
(0, 15),
(0, 16),
(0, 17),
(0, 18),
(0, 19),
(0, 20),
(1, 1),
(1, 4),
(1, 6),
(1, 9),
(1, 11),
(1, 16),
(1, 17),
(2, 2),
(2, 3),
(2, 5),
(2, 7),
(2, 10),
(2, 12),
(2, 15),
(2, 18),
(2, 19),
(2, 20);

INSERT INTO user_role(user_id, role_id) VALUES
(0, 0),
(1, 1),
(2, 2);