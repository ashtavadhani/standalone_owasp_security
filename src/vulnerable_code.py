import sqlite3

def get_user_data(username):
    # CRITICAL OWASP RISK: SQL Injection
    # Direct string formatting allows malicious actors to bypass login checks!
    #query = f"SELECT * FROM users WHERE username = '{username}'"
    
    #conn = sqlite3.connect("database.db")
    #cursor = conn.cursor()
    #cursor.execute(query)
    return cursor.fetchall()
