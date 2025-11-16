
import mysql.connector

CONFIG = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': None,
    'raise_on_warnings': True,
    'use_pure': True,
    'auth_plugin': 'mysql_native_password'
}

DB_NAME = "assignment_db"

def get_conn(db=None):
    cfg = CONFIG.copy()
    if db:
        cfg['database'] = db
    return mysql.connector.connect(
        user=cfg['user'],
        password=cfg['password'],
        host=cfg['host'],
        database=cfg['database'],
        use_pure=cfg['use_pure'],
        auth_plugin=cfg['auth_plugin'],
        connection_timeout=5
    )

if __name__ == "__main__":
    try:
        c = get_conn()
        print("db_helper.py test connection OK")
        c.close()
    except Exception as e:
        print("db_helper.py ERROR:", e)
