Here's the fixed Python code:

```python
import sqlite3

def get_user_data(username):
    # SECURE OWASP RISK: SQL Injection Prevention
    # Use parameterized queries with SQLite or a safer method like ORM.
    query = "SELECT * FROM users WHERE username = ?"
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(query, (username,))
    return cursor.fetchall()
```

This version uses a parameterized query which prevents SQL injection attack[6D[K
attacks. The user input is directly inserted into the prepared statement's [K
parameters, ensuring that it cannot be used to alter the database schema or[2D[K
or execute arbitrary commands.

For a more robust solution, consider using ORM libraries like SQLAlchemy, D[1D[K
Django ORM, etc., which handle all the complexities of SQL and security for[3D[K
for you.