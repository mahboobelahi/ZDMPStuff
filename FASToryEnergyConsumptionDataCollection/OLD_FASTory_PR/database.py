import sqlite3


def create_data_table(name):

    # create a DB connection
    conn = None
    try:
        conn = sqlite3.connect('FASTory_EM_Data.db')
    except sqlite3.Error as e:
        print(e)
    # create a currsor id INTEGER PRIMARY KEY,
    c = conn.cursor()
    sql_cmd = """
    CREATE TABLE IF NOT EXISTS {} (
                "RMS Current (A)" REAL,"RMS Voltage (V)" REAL,PF REAL,
                "Power(KW)" REAL,"Power (W)" REAL,"%Power/Nominal_Power" REAL,
                Label INTEGER, Class INTEGER,
                "Time" timestamp)
                """.format(name)

    c.execute(sql_cmd)
    conn.commit()
    conn.close()

def prediction_Data_table(name):

    # create a DB connection
    conn = None
    try:
        conn = sqlite3.connect('FASTory_EM_Data.db')
    except sqlite3.Error as e:
        print(e)
    # create a currsor id INTEGER PRIMARY KEY,
    c = conn.cursor()
    sql_cmd = """
    CREATE TABLE IF NOT EXISTS {} (
                "Model" TEXT,"T_Class" TEXT,
                 "Power (W)" REAL,"Load_Combination" INTEGER,
                "Active_Zone "TEXT,"M1_Pred" INTEGER, "M2_Pred" INTEGER,
                "Time" timestamp)
                """.format(name)

    c.execute(sql_cmd)
    conn.commit()
    conn.close()

def alert_Column():
    conn = sqlite3.connect('FASTory_EM_Data.db')
    c = conn.cursor()
    sql_cmd = "ALTER TABLE Prediction_Data ADD COLUMN Active_Zone TEXT"
    c.execute(sql_cmd)
    conn.commit()
    conn.close()

def update(data):
    conn = sqlite3.connect('FASTory_EM_Data.db')
    # create a currsor
    c = conn.cursor()
    sql_cmd = "UPDATE Prediction_Data SET Time= ?  WHERE rowid = ?"
    c.execute(sql_cmd,data)
    conn.commit()
    conn.close()

def insert_Pred_data(data):
    conn = sqlite3.connect('FASTory_EM_Data.db')
    # create a currsor
    c = conn.cursor()
    sql_cmd = "INSERT INTO Prediction_Data VALUES (?,?,?,?,?,?,?,?)"
    c.execute(sql_cmd,data)
    conn.commit()
    conn.close()

def insert_EM_data(data):
    conn = sqlite3.connect('FASTory_EM_Data.db')
    # create a currsor
    c = conn.cursor()
    sql_cmd = "INSERT INTO EM_Data VALUES (?,?,?,?,?,?,?,?,?)"
    c.execute(sql_cmd,data)
    conn.commit()
    conn.close()



def fetch_data(id):
    conn = sqlite3.connect('FASTory_EM_Data.db')
    # create a currsor
    c = conn.cursor()
    sql_cmd = "SELECT FROM EM_Data WHERE rowid = (?)"
    c.execute("SELECT * FROM EM_Data WHERE ROWID = (?)",(str(id),))
    i=c.fetchall()
    conn.commit()
    conn.close()
    return i