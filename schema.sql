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
(2, "user", "User", "user");

INSERT INTO permission(id, permission_name) VALUES
(1, "EDIT_DRAFT"),
(2, "EDIT_SUBMITTED"),
(3, "EDIT_APPROVED"),
(4, "EDIT_REJECTED"),
(5, "EDIT_REVOKED"),
(6, "DELETE_DRAFT"),
(7, "DELETE_SUBMITTED"),
(8, "DELETE_APPROVED"),
(9, "DELETE_REJECTED"),
(10, "DELETE_REVOKED"),
(11, "SUBMIT"),
(12, "APPROVE"),
(13, "REJECT"),
(14, "REVOKE");

INSERT INTO role(id, role_name) VALUES
(1, "ADMIN"),
(2, "USER");

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
(2, 1),
(2, 4),
(2, 6),
(2, 9),
(2, 11);

INSERT INTO user_role(user_id, role_id) VALUES
(1, 1),
(2, 2);