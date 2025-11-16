from db_helper import get_conn, DB_NAME

DB = DB_NAME

def late_for_course(course_id):
    conn = get_conn(DB)
    cur = conn.cursor(dictionary=True)
    cur.execute("""
      SELECT s.submission_id, s.assignment_id, s.student_id, s.submitted_at, s.file_path, a.due_date, u.full_name
      FROM submissions s
      JOIN assignments a ON s.assignment_id = a.assignment_id
      JOIN users u ON s.student_id = u.user_id
      WHERE a.course_id = %s AND s.submitted_at > a.due_date
    """, (course_id,))
    rows = cur.fetchall()
    if not rows:
        print('No late submissions found for course', course_id)
    for r in rows:
        print(r['submission_id'], r['assignment_id'], r['student_id'], r['full_name'], r['submitted_at'], 'due:', r['due_date'])
    cur.close(); conn.close()

if __name__ == '__main__':
    late_for_course(1)
