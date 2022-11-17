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
    print(time)
    cur.execute('INSERT INTO monitoring_ids (timestamp) VALUES (?)', (time,))
    id = cur.execute('SELECT * FROM monitoring_ids WHERE timestamp = ?', (time,)).fetchone()[0]
    print(id)
    for cpu_cond in enumerate(cpu, 1):
        cur.execute('INSERT INTO CPU (second, temperature, mon_id) VALUES (?, ?, ?)', (*cpu_cond, id))
    for gpu_cond in enumerate(gpu, 1):
        cur.execute('INSERT INTO GPU (second, temperature, mon_id) VALUES (?, ?, ?)', (*gpu_cond, id))
    con.commit()
    con.close()


def get_monitoring_info(database, name):
    con = sqlite3.connect(database)
    cur = con.cursor()
    CPU_temperatures = cur.execute('SELECT second, temperature FROM CPU WHERE'
                                   ' mon_id = (SELECT id FROM monitoring_ids'
                                   ' WHERE timestamp = ?)', (name,)).fetchall()
    CPU_temperatures = [i[1] for i in CPU_temperatures]
    GPU_temperatures = cur.execute('SELECT second, temperature FROM GPU WHERE'
                                   ' mon_id = (SELECT id FROM monitoring_ids'
                                   ' WHERE timestamp = ?)', (name,)).fetchall()
    GPU_temperatures = [i[1] for i in GPU_temperatures]

    con.close()

    return CPU_temperatures, GPU_temperatures
