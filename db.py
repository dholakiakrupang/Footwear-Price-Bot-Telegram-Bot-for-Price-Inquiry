import sqlite3

DATABASE_NAME = 'bot_database.db'

def get_connection():
    """Get a connection to the database."""
    return sqlite3.connect(DATABASE_NAME)

def init_db():
    """Initialize the database with necessary tables."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS output_mappings (
        input TEXT PRIMARY KEY,
        normal_output TEXT,
        special_output1 TEXT,
        special_output2 TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        user_type TEXT -- 'normal' or 'special'
    )
    ''')
    
    conn.commit()
    conn.close()

def add_output_mapping(input_digit, normal_output, special_output1, special_output2):
    """Add a new output mapping."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO output_mappings (input, normal_output, special_output1, special_output2)
    VALUES (?, ?, ?, ?)
    ''', (input_digit, normal_output, special_output1, special_output2))
    conn.commit()
    conn.close()

def delete_output_mapping(input_digit):
    """Delete an output mapping."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    DELETE FROM output_mappings WHERE input = ?
    ''', (input_digit,))
    conn.commit()
    conn.close()

def update_output_mapping(input_digit, normal_output, special_output1, special_output2):
    """Update an output mapping."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE output_mappings
    SET normal_output = ?, special_output1 = ?, special_output2 = ?
    WHERE input = ?
    ''', (normal_output, special_output1, special_output2, input_digit))
    conn.commit()
    conn.close()

def get_output_mapping(input_digit):
    """Get an output mapping by input digit."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT normal_output, special_output1, special_output2 FROM output_mappings WHERE input = ?
    ''', (input_digit,))
    result = cursor.fetchone()
    conn.close()
    return result

def get_user_type(username):
    """Get user type by username."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT user_type FROM users WHERE username = ?
    ''', (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def add_user(username, user_type):
    """Add a new user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO users (username, user_type)
    VALUES (?, ?)
    ''', (username, user_type))
    conn.commit()
    conn.close()

def delete_user(username):
    """Delete a user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    DELETE FROM users WHERE username = ?
    ''', (username,))
    conn.commit()
    conn.close()

def update_user(username, user_type):
    """Update a user's type."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE users
    SET user_type = ?
    WHERE username = ?
    ''', (user_type, username))
    conn.commit()
    conn.close()
