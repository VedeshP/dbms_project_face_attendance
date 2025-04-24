INSERT INTO DEPARTMENT (DEPT_CODE, DEPT_NAME, SCHOOL_ID) VALUES
    ('CSE', 'Computer Science and Engineering', 'SoT'),
    ('EE', 'Electrical Engineering', 'SoET'),
    ('HUM', 'Humanities', 'SLS'),
    ('MGT', 'Management', 'SoM');


INSERT INTO DEPARTMENT (DEPT_CODE, DEPT_NAME, SCHOOL_ID) VALUES
    ('ICT', 'Information and Communication Technology', 'SoT');

-- add for civil 
-- Insert Civil Department if it doesn't exist
INSERT INTO DEPARTMENT (DEPT_CODE, DEPT_NAME, SCHOOL_ID)
VALUES ('CIV', 'Civil Engineering', 'SoT');

-- mech
INSERT IGNORE INTO DEPARTMENT (DEPT_CODE, DEPT_NAME, SCHOOL_ID)
VALUES ('ME', 'Mechanical Engineering', 'SoT');

-- ece
-- Use 'ECE' for the DEPT_CODE as per common convention for Electronics and Communication
INSERT IGNORE INTO DEPARTMENT (DEPT_CODE, DEPT_NAME, SCHOOL_ID)
VALUES ('ECE', 'Electronics and Communication Engineering', 'SoT');