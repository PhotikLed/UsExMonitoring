import sqlite3

with open('pc_name.txt', encoding='utf8') as text:
    DB_NAME = text.readline() + '.db'


def init_db():
    con = sqlite3.connect(DB_NAME)  # Пишем в БД
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS monitoring_ids(
       id INT PRIMARY KEY AUTOINCREMENT,
       timestamp DATETIME);
        """)
    cur.execute("""CREATE TABLE IF NOT EXISTS CPU(
       second INT PRIMARY KEY,
       temperature INT,
       mon_id INT);
        """)
    cur.execute("""CREATE TABLE IF NOT EXISTS GPU(
       second INT PRIMARY KEY,
       temperature INT,
       mon_id INT);
        """)


def add_monitoring(time, cpu, gpu):
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    cur.execute('INSERT INTO monitoring_ids VALUES (?)', time)
    id = cur.execute('SELECT * FROM monitoring_ids WHERE timestamp = ?', time).fetchone()
    for cpu_cond in enumerate(cpu, 1):
        cur.execute('INSERT INTO CPU (second, temperature, mon_id) VALUES (?, ?, ?)', (*cpu_cond, id))
    for gpu_cond in enumerate(gpu, 1):
        cur.execute('INSERT INTO GPU (second, temperature, mon_id) VALUES (?, ?, ?)', (*gpu_cond, id))
    con.commit()
    con.close()
