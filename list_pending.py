from db_helper import get_conn, DB_NAME

DB = DB_NAME

def pending(course_id, assignment_id):
    conn = get_conn(DB)
    cur = conn.cursor(dictionary=True)
    cur.execute("""
      SELECT u.user_id, u.full_name
      FROM enrollments e
      JOIN users u ON e.student_id = u.user_id
      LEFT JOIN submissions s ON s.student_id = u.user_id AND s.assignment_id = %s
      WHERE e.course_id = %s AND s.submission_id IS NULL
    """, (assignment_id, course_id))
    rows = cur.fetchall()
    if not rows:
        print('No pending students (or check IDs).')
    for r in rows:
        print(r['user_id'], r['full_name'])
    cur.close(); conn.close()

if __name__ == '__main__':
    pending(1, 1)
