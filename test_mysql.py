# scripts/test_mysql.py
import mysql.connector
import sys

print("STARTING MYSQL TEST (force native auth + TCP)")

try:
    conn = mysql.connector.connect(
        host="127.0.0.1",            # force TCP
        user="root",
        password="",                 # put password here if you have one
        connection_timeout=5,
        use_pure=True,
        auth_plugin='mysql_native_password'
    )
    print("CONNECTED to MySQL/MariaDB via mysql-connector!")
    cur = conn.cursor()
    cur.execute("SHOW DATABASES;")
    for r in cur.fetchall():
        print(" -", r[0])
    conn.close()
    print("DONE")
except Exception as e:
    print("MYSQL ERROR:", repr(e))
    sys.exit(1)
