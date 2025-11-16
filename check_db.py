
from db_helper import get_conn
import sys

try:
    conn = get_conn()   
    cur = conn.cursor()
    cur.execute("SHOW DATABASES;")
    dbs = [r[0] for r in cur.fetchall()]
    print("Databases on MySQL server:")
    for d in dbs:
        print(" -", d)
    cur.close()
    conn.close()
except Exception as e:
    print("ERROR:", repr(e))
    sys.exit(1)
