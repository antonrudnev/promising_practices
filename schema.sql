DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS permission;
DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS role_permission;
DROP TABLE IF EXISTS user_role;

DROP TABLE IF EXISTS user_comment;
DROP TABLE IF EXISTS user_mention;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_name TEXT UNIQUE NOT NULL,
  full_name TEXT NOT NULL,
  password TEXT NOT NULL,
  enabled INTEGER DEFAULT 1,
  last_login TIMESTAMP,
  created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

CREATE TABLE user_comment (
  id INTEGER PRIMARY KEY,
  document_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  comment TEXT NOT NULL,
  created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE user_mention (
  user_id INTEGER NOT NULL,
  user_comment_id INTEGER NOT NULL,
  was_read INTEGER DEFAULT 0,
  was_deleted INTEGER DEFAULT 0,
  created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES user (id),
  FOREIGN KEY (user_comment_id) REFERENCES role (id),
  PRIMARY KEY (user_id, user_comment_id)
);

INSERT INTO user (id, user_name, full_name, password) VALUES
(0, "admin", "Administrator", "admin"),
(1, "data", "Data Operator", "data"),
(2, "qa", "Validation Engineer", "qa");

INSERT INTO permission(id, permission_name) VALUES
(0, "VIEW_DRAFT"),
(1, "VIEW_SUBMITTED"),
(2, "VIEW_APPROVED"),
(3, "VIEW_REJECTED"),
(4, "VIEW_REVOKED"),
(5, "EDIT_DRAFT"),
(6, "EDIT_SUBMITTED"),
(7, "EDIT_APPROVED"),
(8, "EDIT_REJECTED"),
(9, "EDIT_REVOKED"),
(10, "DELETE_DRAFT"),
(11, "DELETE_SUBMITTED"),
(12, "DELETE_APPROVED"),
(13, "DELETE_REJECTED"),
(14, "DELETE_REVOKED"),
(15, "ACTION_CREATE"),
(16, "ACTION_SUBMIT"),
(17, "ACTION_APPROVE"),
(18, "ACTION_REJECT"),
(19, "ACTION_REVOKE"),
(20, "SECURITY_ADMIN");

INSERT INTO role(id, role_name) VALUES
(0, "ADMINISTRATOR"),
(1, "DATA_ENTRY_OPERATOR"),
(2, "DATA_VALIDATION_ENGINEER");

INSERT INTO role_permission(role_id, permission_id) VALUES
(0, 20),
(1, 0),
(1, 3),
(1, 5),
(1, 8),
(1, 10),
(1, 15),
(1, 16),
(2, 1),
(2, 2),
(2, 4),
(2, 6),
(2, 9),
(2, 11),
(2, 14),
(2, 17),
(2, 18),
(2, 19);

INSERT INTO user_role(user_id, role_id) VALUES
(0, 0),
(0, 1),
(0, 2),
(1, 1),
(2, 2);