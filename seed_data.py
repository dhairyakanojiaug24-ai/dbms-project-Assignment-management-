# scripts/seed_data.py
# Robust, very-verbose seeder for assignment_project
from db_helper import get_conn, DB_NAME
from datetime import datetime, timedelta
import sys
import traceback

def safe_exec(conn, sql, params=None, desc=None):
    cur = conn.cursor()
    try:
        if desc:
            print("  ->", desc)
        cur.execute(sql, params or ())
        conn.commit()
        return True, cur
    except Exception as e:
        print("  ERROR executing SQL:", desc or sql)
        traceback.print_exc()
        conn.rollback()
        cur.close()
        return False, None

def main():
    print("SEED: Starting seeding process")
    try:
        # test connection without DB
        conn0 = get_conn()
        print("SEED: Connected to server (no DB selected).")
        conn0.close()
    except Exception as e:
        print("SEED: Could NOT connect to server. Error:")
        traceback.print_exc()
        sys.exit(1)

    # connect to project DB (will raise if DB missing)
    try:
        conn = get_conn(DB_NAME)
        print(f"SEED: Connected to database '{DB_NAME}'.")
    except Exception as e:
        print(f"SEED: Failed to connect to database '{DB_NAME}'. Error:")
        traceback.print_exc()
        sys.exit(1)

    try:
        # 1) Insert users (instructor + 2 students)
        print("\nSEED: Inserting users...")
        users_sql = "INSERT IGNORE INTO users (username, full_name, email, role) VALUES (%s,%s,%s,%s)"
        for u in [
            ("inst1", "Prof. A", "inst1@example.com", "instructor"),
            ("stud1", "Student One", "s1@example.com", "student"),
            ("stud2", "Student Two", "s2@example.com", "student"),
        ]:
            ok, _ = safe_exec(conn, users_sql, u, desc=f"insert user {u[0]}")
            if not ok:
                print("SEED: continuing despite user insert error...")

        # confirm users
        cur = conn.cursor()
        cur.execute("SELECT user_id, username, role FROM users WHERE username IN ('inst1','stud1','stud2')")
        rows = cur.fetchall()
        print("SEED: Users present after insert:", rows)
        cur.close()

        # 2) Get instructor id
        cur = conn.cursor()
        cur.execute("SELECT user_id FROM users WHERE username=%s LIMIT 1", ("inst1",))
        row = cur.fetchone()
        if not row:
            print("SEED: ERROR - instructor 'inst1' not found. Aborting.")
            cur.close()
            conn.close()
            sys.exit(1)
        inst_id = row[0]
        print("SEED: instructor id:", inst_id)
        cur.close()

        # 3) Insert course
        print("\nSEED: Inserting course CS101...")
        course_sql = "INSERT IGNORE INTO courses (course_code, title, instructor_id) VALUES (%s,%s,%s)"
        ok, _ = safe_exec(conn, course_sql, ("CS101", "Intro to DBMS", inst_id), desc="insert course CS101")
        if not ok:
            print("SEED: course insert reported error (but will continue).")

        # show courses
        cur = conn.cursor()
        cur.execute("SELECT course_id, course_code, title, instructor_id FROM courses WHERE course_code=%s", ("CS101",))
        courses = cur.fetchall()
        print("SEED: Courses matching CS101:", courses)
        cur.close()

        if not courses:
            print("SEED: ERROR - course CS101 not found after insert. Aborting.")
            conn.close()
            sys.exit(1)
        cid = courses[0][0]

        # 4) Get student ids
        cur = conn.cursor()
        cur.execute("SELECT user_id FROM users WHERE username=%s", ("stud1",))
        s1 = cur.fetchone()
        cur.execute("SELECT user_id FROM users WHERE username=%s", ("stud2",))
        s2 = cur.fetchone()
        if not s1 or not s2:
            print("SEED: ERROR - one or both student ids missing:", s1, s2)
            cur.close(); conn.close(); sys.exit(1)
        s1 = s1[0]; s2 = s2[0]
        print("SEED: student ids:", s1, s2)
        cur.close()

        # 5) Insert enrollments
        print("\nSEED: Inserting enrollments...")
        enroll_sql = "INSERT IGNORE INTO enrollments (course_id, student_id) VALUES (%s,%s)"
        safe_exec(conn, enroll_sql, (cid, s1), desc=f"enroll stud1 -> course {cid}")
        safe_exec(conn, enroll_sql, (cid, s2), desc=f"enroll stud2 -> course {cid}")

        # show enrollments
        cur = conn.cursor()
        cur.execute("SELECT enrollment_id, course_id, student_id FROM enrollments WHERE course_id=%s", (cid,))
        print("SEED: enrollments for course", cid, "->", cur.fetchall())
        cur.close()

        # 6) Insert assignment due tomorrow
        print("\nSEED: Inserting assignment for course", cid)
        due = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        assign_sql = "INSERT IGNORE INTO assignments (course_id, title, description, due_date) VALUES (%s,%s,%s,%s)"
        safe_exec(conn, assign_sql, (cid, "Assignment 1", "Implement ER diagram and SQL", due), desc="insert Assignment 1")


        cur = conn.cursor()
        cur.execute("SELECT assignment_id, course_id, title, due_date FROM assignments WHERE course_id=%s", (cid,))
        print("SEED: assignments for course", cid, "->", cur.fetchall())
        cur.close()

        print("\nSEED: Final table counts:")
        cur = conn.cursor()
        for t in ["users", "courses", "enrollments", "assignments", "submissions"]:
            cur.execute(f"SELECT COUNT(*) FROM {t}")
            c = cur.fetchone()[0]
            print(f"  {t}: {c}")
        cur.close()

        print("\nSEED: insertion complete.")
    except Exception as e:
        print("SEED: UNEXPECTED ERROR:")
        traceback.print_exc()
    finally:
        try:
            conn.close()
        except:
            pass

if __name__ == "__main__":
    main()
