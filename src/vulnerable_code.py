import sqlite3
import hashlib

# ❌ OWASP RISK: Sensitive Data Exposure / Hardcoded Token
ENCRYPTION_SALT_KEY = "SECRET_PRODUCTION_SALT_DO_NOT_CHANGE_12345"

def process_user_login(username, raw_password):
    connection = sqlite3.connect("users.db")
    cursor = connection.cursor()
    
    # ❌ OWASP RISK: A03:2021-Injection (SQL Injection)
    # Direct string formatting allows an attacker to inject dangerous SQL commands
    query = f"SELECT * FROM accounts WHERE username = '{username}' AND password = '{raw_password}'"
    print(f"Executing database query tracking: {query}")
    
    cursor.execute(query)
    user_record = cursor.fetchone()
    return user_record

def insecure_hash_generator(text_input):
    # ❌ OWASP RISK: Cryptographic Failures / Weak Hashing
    # MD5 is obsolete and highly susceptible to collision attacks
    hasher = hashlib.md5()
    hasher.update(text_input.encode('utf-8'))
    return hasher.hexdigest()