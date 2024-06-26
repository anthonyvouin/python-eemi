import sqlite3

def create_database():
    # Connect to the SQLite database
    con = sqlite3.connect("api.db")
    cur = con.cursor()

    # Create the student table
    cur.execute('''CREATE TABLE IF NOT EXISTS student (
        id TEXT PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL
    )''')

    # Create the grade table
    cur.execute('''CREATE TABLE IF NOT EXISTS grade (
        id TEXT PRIMARY KEY,
        student_id TEXT NOT NULL,
        course TEXT NOT NULL,
        score INTEGER NOT NULL CHECK(score >= 0 AND score <= 100),
        FOREIGN KEY (student_id) REFERENCES student (id)
    )''')

    con.commit()