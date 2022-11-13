import sqlite3

with open('pc_name.txt', encoding='utf8') as text:
    DB_NAME = text.readline() + '.db'


def init_db():
    con = sqlite3.connect(DB_NAME)  # Пишем в БД
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS monitoring_ids(
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       timestamp TEXT);
        """)
    cur.execute("""CREATE TABLE IF NOT EXISTS CPU(
       table_id INTEGER PRIMARY KEY AUTOINCREMENT,
       second INT,
       temperature INT,
       mon_id INT);
        """)
    cur.execute("""CREATE TABLE IF NOT EXISTS GPU(
       table_id INTEGER PRIMARY KEY AUTOINCREMENT,
       second INT,
       temperature INT,
       mon_id INT);
        """)


def add_monitoring(time: str, cpu, gpu):
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    time = ':'.join(time.split(':')[:2])
    cur.execute('INSERT INTO monitoring_ids (timestamp) VALUES (?)', (time,))
    id = cur.execute('SELECT * FROM monitoring_ids WHERE timestamp = ?', (time,)).fetchone()[0]
    print(id)
    for cpu_cond in enumerate(cpu, 1):
        cur.execute('INSERT INTO CPU (second, temperature, mon_id) VALUES (?, ?, ?)', (*cpu_cond, id))
    for gpu_cond in enumerate(gpu, 1):
        cur.execute('INSERT INTO GPU (second, temperature, mon_id) VALUES (?, ?, ?)', (*gpu_cond, id))
    con.commit()
    con.close()
