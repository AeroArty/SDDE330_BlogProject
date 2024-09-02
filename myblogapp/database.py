import sqlite3
from datetime import datetime

db_name = 'myblog.db'

def create_author(username, email, password, bio, profile_picture):
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Author (username, email, password, bio, profile_picture)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, email, password, bio, profile_picture))
            conn.commit()
            return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None
def get_author(user_id):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Author WHERE user_id=?', (user_id,))
        return cursor.fetchone()

def update_author(user_id, username, email, bio, profile_picture):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Author SET username=?, email=?, bio=?, profile_picture=?
            WHERE user_id=?
        ''', (username, email, bio, profile_picture, user_id))
        conn.commit()
        return cursor.rowcount

def delete_author(user_id):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Author WHERE user_id=?', (user_id,))
        conn.commit()
        return cursor.rowcount

def create_blog_entry(user_id, title, subtitle, blurb, content, is_published):
    time_created = datetime.now()
    time_updated = time_created
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO BlogEntry (user_id, title, subtitle, blurb, content, time_created, time_updated, is_published)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, title, subtitle, blurb, content, time_created, time_updated, is_published))
        conn.commit()
        return cursor.lastrowid, time_created

def get_blog_entry(post_id):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM BlogEntry WHERE post_id=?', (post_id,))
        return cursor.fetchone()

def get_blog_entries():
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM BlogEntry")
        return cursor.fetchall()

def update_blog_entry(post_id, title, subtitle, blurb, content, is_published):
    time_updated = datetime.now()
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE BlogEntry SET title=?, subtitle=?, blurb=?, content=?, time_updated=?, is_published=?
            WHERE post_id=?
        ''', (title, subtitle, blurb, content, time_updated, is_published, post_id))
        conn.commit()
        return cursor.rowcount, time_updated

def delete_blog_entry(post_id):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM BlogEntry WHERE post_id=?', (post_id,))
        conn.commit()
        return cursor.rowcount
