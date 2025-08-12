-- ALTER TABLE users ADD COLUMN contact_number TEXT;
-- ALTER TABLE users ADD COLUMN email_address TEXT;/*  */
-- ALTER TABLE users ADD COLUMN blood_group TEXT;
-- ALTER TABLE users ADD COLUMN is_disabled BOOLEAN DEFAULT 0;
-- ALTER TABLE users ADD COLUMN disability_type TEXT;


-- ALTER TABLE users ADD COLUMN has_12th BOOLEAN DEFAULT 0;
-- ALTER TABLE users ADD COLUMN `12th_stream` TEXT;
-- ALTER TABLE users ADD COLUMN `12th_percentage` REAL;
-- ALTER TABLE users ADD COLUMN `12th_year` INTEGER;
-- ALTER TABLE users ADD COLUMN `12th_school` TEXT;
-- ALTER TABLE users ADD COLUMN `12th_board` TEXT;

-- ALTER TABLE users ADD COLUMN has_graduation BOOLEAN DEFAULT 0;
-- ALTER TABLE users ADD COLUMN graduation_degree TEXT;
-- ALTER TABLE users ADD COLUMN graduation_specialization TEXT;
-- ALTER TABLE users ADD COLUMN graduation_cgpa REAL;
-- ALTER TABLE users ADD COLUMN graduation_college TEXT;
-- ALTER TABLE users ADD COLUMN graduation_year INTEGER;

-- ALTER TABLE users ADD COLUMN has_pg BOOLEAN DEFAULT 0;
-- ALTER TABLE users ADD COLUMN pg_degree TEXT;
-- ALTER TABLE users ADD COLUMN pg_specialization TEXT;
-- ALTER TABLE users ADD COLUMN pg_cgpa REAL;
-- ALTER TABLE users ADD COLUMN pg_college TEXT;
-- ALTER TABLE users ADD COLUMN pg_year INTEGER;

-- ALTER TABLE users ADD COLUMN has_phd BOOLEAN DEFAULT 0;
-- ALTER TABLE users ADD COLUMN phd_field TEXT;
-- ALTER TABLE users ADD COLUMN phd_specialization TEXT;
-- ALTER TABLE users ADD COLUMN phd_status TEXT;
-- ALTER TABLE users ADD COLUMN phd_university TEXT;
-- ALTER TABLE users ADD COLUMN phd_year INTEGER;
-- ALTER TABLE users ADD COLUMN phd_thesis TEXT;

-- CREATE UNIQUE INDEX IF NOT EXISTS idx_employee_number ON users(employee_number);

-- ALTER TABLE users ADD COLUMN office TEXT;
-- ALTER TABLE users ADD COLUMN designation TEXT;
-- ALTER TABLE users ADD COLUMN employee_type TEXT;
-- ALTER TABLE users ADD COLUMN subgroup TEXT;
-- ALTER TABLE users ADD COLUMN class INTEGER;

