from db_helper import get_conn, DB_NAME
import mysql.connector
print("running create_schema.py")

TABLES = {}
TABLES['users'] = (
    "CREATE TABLE IF NOT EXISTS users ("
    "  user_id INT AUTO_INCREMENT PRIMARY KEY,"
    "  username VARCHAR(50) UNIQUE NOT NULL,"
    "  full_name VARCHAR(100) NOT NULL,"
    "  email VARCHAR(100) UNIQUE,"
    "  role ENUM('student','instructor','admin') NOT NULL,"
    "  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    ") ENGINE=InnoDB"
)

TABLES['courses'] = (
    "CREATE TABLE IF NOT EXISTS courses ("
    " course_id INT AUTO_INCREMENT PRIMARY KEY,"
    " course_code VARCHAR(20) UNIQUE NOT NULL,"
    " title VARCHAR(150) NOT NULL,"
    " instructor_id INT NOT NULL,"
    " start_date DATE,"
    " end_date DATE,"
    " FOREIGN KEY (instructor_id) REFERENCES users(user_id)"
    ") ENGINE=InnoDB"
)

TABLES['enrollments'] = (
    "CREATE TABLE IF NOT EXISTS enrollments ("
    " enrollment_id INT AUTO_INCREMENT PRIMARY KEY,"
    " course_id INT NOT NULL,"
    " student_id INT NOT NULL,"
    " UNIQUE KEY uq_enroll(course_id, student_id),"
    " FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,"
    " FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE"
    ") ENGINE=InnoDB"
)

TABLES['assignments'] = (
    "CREATE TABLE IF NOT EXISTS assignments ("
    " assignment_id INT AUTO_INCREMENT PRIMARY KEY,"
    " course_id INT NOT NULL,"
    " title VARCHAR(200) NOT NULL,"
    " description TEXT,"
    " posted_date DATETIME DEFAULT CURRENT_TIMESTAMP,"
    " due_date DATETIME NOT NULL,"
    " max_marks INT DEFAULT 100,"
    " FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE"
    ") ENGINE=InnoDB"
)

TABLES['submissions'] = (
    "CREATE TABLE IF NOT EXISTS submissions ("
    " submission_id INT AUTO_INCREMENT PRIMARY KEY,"
    " assignment_id INT NOT NULL,"
    " student_id INT NOT NULL,"
    " submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,"
    " file_path VARCHAR(255),"
    " is_late BOOLEAN DEFAULT FALSE,"
    " UNIQUE KEY uq_sub(assignment_id, student_id),"
    " FOREIGN KEY (assignment_id) REFERENCES assignments(assignment_id) ON DELETE CASCADE,"
    " FOREIGN KEY (student_id) REFERENCES users(user_id) ON DELETE CASCADE"
    ") ENGINE=InnoDB"
)
TABLES['grades'] = (
    "CREATE TABLE IF NOT EXISTS grades ("
    " grade_id INT AUTO_INCREMENT PRIMARY KEY,"
    " submission_id INT NOT NULL,"
    " grader_id INT NOT NULL,"
    " marks_obtained DECIMAL(5,2),"
    " feedback TEXT,"
    " graded_at DATETIME DEFAULT CURRENT_TIMESTAMP,"
    " FOREIGN KEY (submission_id) REFERENCES submissions(submission_id) ON DELETE CASCADE,"
    " FOREIGN KEY (grader_id) REFERENCES users(user_id)"
    ") ENGINE=InnoDB"
)
def create_database(cursor):
    try:
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET 'utf8mb4'")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        raise

def main():
    conn = get_conn()
    cursor = conn.cursor()
    create_database(cursor)
    conn.database = DB_NAME
    for name, ddl in TABLES.items():
        try:
            print(f"Creating table {name}...", end='')
            cursor.execute(ddl)
            print('OK')
        except mysql.connector.Error as err:
            print(f"Failed creating table {name}: {err.msg}")
    cursor.close()
    conn.close()
    print('Schema creation complete.')
if __name__ == '__main__':
    main()
