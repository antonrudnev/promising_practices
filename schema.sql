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
(1, "admin", "Administrator", "admin"),
(2, "data", "Data Operator", "data"),
(3, "qa", "QA Engineer", "qa");

INSERT INTO permission(id, permission_name) VALUES
(1, "VIEW_DRAFT"),
(2, "VIEW_SUBMITTED"),
(3, "VIEW_APPROVED"),
(4, "VIEW_REJECTED"),
(5, "VIEW_REVOKED"),
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
(1, "ADMINISTRATOR"),
(2, "DATA_ENTRY"),
(3, "DATA_VALIDATION");

INSERT INTO role_permission(role_id, permission_id) VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 4),
(1, 5),
(1, 6),
(1, 7),
(1, 8),
(1, 9),
(1, 10),
(1, 11),
(1, 12),
(1, 13),
(1, 14),
(1, 15),
(1, 16),
(1, 17),
(1, 18),
(1, 19),
(1, 20),
(2, 1),
(2, 4),
(2, 6),
(2, 9),
(2, 11),
(2, 16),
(2, 17),
(3, 2),
(3, 3),
(3, 5),
(3, 7),
(3, 10),
(3, 12),
(3, 15),
(3, 18),
(3, 19),
(3, 20);

INSERT INTO user_role(user_id, role_id) VALUES
(1, 1),
(2, 2),
(3, 4);