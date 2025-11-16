import os
import shutil
from datetime import datetime
from db_helper import get_conn, DB_NAME

DB = DB_NAME
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
UPLOAD_DIR = os.path.join(PROJECT_ROOT, 'uploads')

def submit(assignment_id, student_id, source_file):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = f"{assignment_id}_{student_id}_{ts}_" + os.path.basename(source_file)
    dest = os.path.join(UPLOAD_DIR, filename)
    shutil.copyfile(source_file, dest)

    conn = get_conn(DB)
    cur = conn.cursor()
    cur.execute("SELECT due_date FROM assignments WHERE assignment_id=%s", (assignment_id,))
    row = cur.fetchone()
    if not row:
        print('Assignment not found. Check assignment_id')
        cur.close(); conn.close(); return
    due = row[0]
    now = datetime.now()
    is_late = now > due

    cur.execute(
        "INSERT INTO submissions (assignment_id, student_id, submitted_at, file_path, is_late) VALUES (%s,%s,%s,%s,%s)",
        (assignment_id, student_id, now.strftime('%Y-%m-%d %H:%M:%S'), dest, is_late)
    )
    conn.commit()
    print('Submitted:', dest, 'is_late=', is_late)
    cur.close(); conn.close()

if __name__ == '__main__':
    assignment_id = 1
    student_id = 2
    sample = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sample_submission.pdf')
    if not os.path.exists(sample):
        with open(sample, 'w') as f:
            f.write('This is a sample submission file. Replace with a real PDF for demo.')
        print('Created placeholder sample_submission.pdf at project root.')
    submit(assignment_id, student_id, sample)
