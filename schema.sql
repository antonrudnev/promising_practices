DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS permission;
DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS role_permission;
DROP TABLE IF EXISTS user_role;
DROP TABLE IF EXISTS master_data;
DROP TABLE IF EXISTS user_comment;
DROP TABLE IF EXISTS user_mention;


CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_name TEXT UNIQUE NOT NULL,
  full_name TEXT NOT NULL,
  password TEXT NOT NULL,
  is_enabled INTEGER DEFAULT 1,
  last_login TIMESTAMP,
  created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE permission (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  permission_name TEXT UNIQUE NOT NULL
);


CREATE TABLE role (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
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


CREATE TABLE master_data (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  category TEXT NOT NULL,
  value TEXT NOT NULL,
  order_number INTEGER DEFAULT 0,
  UNIQUE (category, value) ON CONFLICT REPLACE
);


CREATE TABLE user_comment (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  document_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  comment TEXT NOT NULL,
  created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE
);


CREATE TABLE user_mention (
  user_id INTEGER NOT NULL,
  user_comment_id INTEGER NOT NULL,
  was_read INTEGER DEFAULT 0,
  was_deleted INTEGER DEFAULT 0,
  FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE,
  FOREIGN KEY (user_comment_id) REFERENCES role (id) ON DELETE CASCADE,
  PRIMARY KEY (user_id, user_comment_id)
);


INSERT INTO user (id, user_name, full_name, password) VALUES
(0, 'admin', 'Administrator', 'admin');


INSERT INTO permission(id, permission_name) VALUES
(0, 'VIEW_DRAFT'),
(1, 'VIEW_SUBMITTED'),
(2, 'VIEW_APPROVED'),
(3, 'VIEW_REJECTED'),
(4, 'VIEW_REVOKED'),
(5, 'EDIT_DRAFT'),
(6, 'EDIT_SUBMITTED'),
(7, 'EDIT_APPROVED'),
(8, 'EDIT_REJECTED'),
(9, 'EDIT_REVOKED'),
(10, 'DELETE_DRAFT'),
(11, 'DELETE_SUBMITTED'),
(12, 'DELETE_APPROVED'),
(13, 'DELETE_REJECTED'),
(14, 'DELETE_REVOKED'),
(15, 'ACTION_CREATE'),
(16, 'ACTION_SUBMIT'),
(17, 'ACTION_APPROVE'),
(18, 'ACTION_REJECT'),
(19, 'ACTION_REVOKE'),
(20, 'ADMIN_SECURITY'),
(21, 'ADMIN_CONTENT'),
(22, 'ADMIN_MASTERDATA');

INSERT INTO role(id, role_name) VALUES
(0, 'administrator'),
(1, 'data_entry'),
(2, 'data_validation'),
(3, 'supervisor');


INSERT INTO role_permission(role_id, permission_id) VALUES
(0, 20),
(0, 21),
(0, 22),
(1, 0),
(1, 3),
(1, 5),
(1, 8),
(1, 10),
(1, 13),
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
(2, 19),
(3, 0),
(3, 1),
(3, 2),
(3, 3),
(3, 4);


INSERT INTO user_role(user_id, role_id) VALUES
(0, 0),
(0, 3);


INSERT INTO master_data(category, value) VALUES
('COUNTRIES', 'Domestic'),
('COUNTRIES', 'International'),
('IMPLEMENTERS', 'Health Care Providers'),
('IMPLEMENTERS', 'Mental Health Care Providers'),
('IMPLEMENTERS', 'Pharmacists'),
('IMPLEMENTERS', 'State Officials'),
('IMPLEMENTERS', 'Community Officials'),
('IMPLEMENTERS', 'Federal Officials'),
('IMPLEMENTERS', 'County Officials'),
('IMPLEMENTERS', 'Police'),
('IMPLEMENTERS', 'Courts'),
('IMPLEMENTERS', 'Schools'),
('IMPLEMENTERS', 'Correctional Institutions'),
('IMPLEMENTERS', 'Faith Communities'),
('IMPLEMENTERS', 'First Responders'),
('IMPLEMENTERS', 'Child Welfare'),
('IMPLEMENTERS', 'Juvenile Justice'),
('IMPLEMENTERS', 'Recovery Community'),
('IMPLEMENTERS', 'Public Health Officials'),
('IMPLEMENTERS', 'Anti-Drug Coalition'),
('IMPLEMENTERS', 'Non-Governmental Community Organization'),
('INTERVENTION_GOALS', 'Prevention'),
('INTERVENTION_GOALS', 'Harm Reduction'),
('INTERVENTION_GOALS', 'Treatment'),
('INTERVENTION_GOALS', 'Recovery'),
('INTERVENTION_NAMES', 'Prescription Drug Monitoring Programs'),
('INTERVENTION_NAMES', 'Family Functional Therapy'),
('INTERVENTION_NAMES', 'Multi-Dimensional Family Therapy'),
('INTERVENTION_NAMES', 'Cognitive Behavioral Therapy'),
('INTERVENTION_NAMES', 'Hub and Spoke Model'),
('INTERVENTION_NAMES', 'Co-Prescription of Naloxone'),
('INTERVENTION_NAMES', 'Integration of PDMP and EHR'),
('INTERVENTION_NAMES', 'Community Distribution of Naloxone'),
('INTERVENTION_NAMES', 'Layperson Training in Administration of Naloxone'),
('INTERVENTION_NAMES', 'Drug Disposal Programs'),
('INTERVENTION_NAMES', 'Prescription of Naloxone in ER'),
('INTERVENTION_NAMES', 'Safe Storage Programs'),
('INTERVENTION_NAMES', 'Use of Naloxone by First Responders'),
('INTERVENTION_NAMES', 'Providing Naloxone Upon Release from Correctional Facilities'),
('INTERVENTION_NAMES', 'Safe Consumption Sites'),
('INTERVENTION_NAMES', 'Syringe Services'),
('INTERVENTION_NAMES', 'Lock-In Programs'),
('INTERVENTION_NAMES', 'Recovery Programs and Support Groups'),
('INTERVENTION_NAMES', 'Drug Courts'),
('INTERVENTION_NAMES', 'Treatment in Correctional Institutions'),
('INTERVENTION_NAMES', 'Employment for People in Recovery'),
('INTERVENTION_NAMES', 'Youth Education Program'),
('INTERVENTION_NAMES', 'Helpline'),
('INTERVENTION_NAMES', 'Contingency Management'),
('INTERVENTION_NAMES', 'Naloxone Distribution at Pharmacies'),
('INTERVENTION_NAMES', 'Support or Educational Programs in Correctional Facilities'),
('INTERVENTION_NAMES', 'Tele-Health'),
('INTERVENTION_NAMES', 'Social Media'),
('INTERVENTION_NAMES', 'Public Awareness Campaign'),
('INTERVENTION_NAMES', 'Family Education Programs'),
('INTERVENTION_NAMES', 'Pharmacotherapy Related Programs & Policies'),
('INTERVENTION_NAMES', 'Fentanyl Testing Kits'),
('INTERVENTION_NAMES', 'Offering Pharmacotherapy to High Risk Individuals at the ER'),
('INTERVENTION_NAMES', 'Other'),
('POPULATIONS', 'General'),
('POPULATIONS', 'Adults'),
('POPULATIONS', 'Youth'),
('POPULATIONS', 'Pregnant Women'),
('POPULATIONS', 'Women of Childbearing Age'),
('POPULATIONS', 'Neonates'),
('POPULATIONS', 'Not Specified'),
('PROGRAM_COMPONENTS', 'Cognitive Behavioral Therapy'),
('PROGRAM_COMPONENTS', 'Naloxone'),
('PROGRAM_COMPONENTS', 'Training'),
('PROGRAM_COMPONENTS', 'Policy'),
('PROGRAM_COMPONENTS', 'Medication Assisted Treatment'),
('PROGRAM_COMPONENTS', 'Pharmacotherapy'),
('PROGRAM_COMPONENTS', 'Behavioral'),
('PROGRAM_COMPONENTS', 'Mental Health'),
('PROGRAM_COMPONENTS', 'Communication'),
('PROGRAM_COMPONENTS', 'Prescription Drug Monitoring Program'),
('PROGRAM_COMPONENTS', 'Epidemiological Surveillance'),
('PROGRAM_COMPONENTS', 'Remote or Tele-Medicine'),
('PROGRAM_COMPONENTS', 'Recovery Program'),
('PROGRAM_COMPONENTS', 'Incentives'),
('PROGRAM_COMPONENTS', 'Transportation'),
('PROGRAM_COMPONENTS', 'Housing'),
('PROGRAM_COMPONENTS', 'Prescription Drug Disposal'),
('PROGRAM_COMPONENTS', 'Lock-In'),
('PROGRAM_COMPONENTS', 'Syringe Services'),
('PROGRAM_COMPONENTS', 'Prescription Drug Storage'),
('PROGRAM_COMPONENTS', 'Supervised Consumption Sites'),
('PROGRAM_COMPONENTS', 'Outreach'),
('PROGRAM_COMPONENTS', 'Family Involvement'),
('PROGRAM_COMPONENTS', 'Wrap-Around Services'),
('PROGRAM_COMPONENTS', 'Peer-Support'),
('PROGRAM_COMPONENTS', 'Hub and Spoke'),
('PROGRAM_SUCCESSES', 'Significant Improvement'),
('PROGRAM_SUCCESSES', 'No Significant Change'),
('PROGRAM_SUCCESSES', 'Significant Decline'),
('PROGRAM_SUCCESSES', 'Findings Mixed'),
('PROGRAM_SUCCESSES', 'No Evaluation'),
('PROGRAM_SUCCESSES', 'Clearinghouse Endorsement'),
('RACES', 'Black or African American'),
('RACES', 'White'),
('RACES', 'Asian or Pacific Islander'),
('RACES', 'American Indian or Alaska Native'),
('RACES', 'Hispanic or Latino'),
('REGIONS', 'Urban'),
('REGIONS', 'Rural'),
('REGIONS', 'Suburban'),
('REGIONS', 'Not Specified'),
('REGIONS', 'General'),
('SCALES', 'Community'),
('SCALES', 'County'),
('SCALES', 'State'),
('SCALES', 'Federal'),
('SOURCE_TYPES', 'Community Example'),
('SOURCE_TYPES', 'Published Literature'),
('SOURCE_TYPES', 'Report'),
('SOURCE_TYPES', 'Clearinghouse'),
('SOURCE_TYPES', 'Systematic Review'),
('SOURCE_TYPES', 'Recommendations from Government'),
('SOURCE_TYPES', 'Recommendations from Non-Governmental Group'),
('SOURCE_TYPES', 'Other'),
('STATES', 'AL'),
('STATES', 'AK'),
('STATES', 'AZ'),
('STATES', 'AR'),
('STATES', 'CA'),
('STATES', 'CO'),
('STATES', 'CT'),
('STATES', 'DC'),
('STATES', 'DE'),
('STATES', 'FL'),
('STATES', 'GA'),
('STATES', 'HI'),
('STATES', 'ID'),
('STATES', 'IL'),
('STATES', 'IN'),
('STATES', 'IA'),
('STATES', 'KS'),
('STATES', 'KY'),
('STATES', 'LA'),
('STATES', 'ME'),
('STATES', 'MD'),
('STATES', 'MA'),
('STATES', 'MI'),
('STATES', 'MN'),
('STATES', 'MS'),
('STATES', 'MO'),
('STATES', 'MT'),
('STATES', 'NE'),
('STATES', 'NV'),
('STATES', 'NH'),
('STATES', 'NJ'),
('STATES', 'NM'),
('STATES', 'NY'),
('STATES', 'NC'),
('STATES', 'ND'),
('STATES', 'OH'),
('STATES', 'OK'),
('STATES', 'OR'),
('STATES', 'PA'),
('STATES', 'SC'),
('STATES', 'SD'),
('STATES', 'TN'),
('STATES', 'TX'),
('STATES', 'UT'),
('STATES', 'VT'),
('STATES', 'VA'),
('STATES', 'WA'),
('STATES', 'WV'),
('STATES', 'WI'),
('STATES', 'WY');

UPDATE master_data
SET order_number = id * 5;