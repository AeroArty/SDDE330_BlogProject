from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
db_name = 'myblog.db'

def init_db():
    pass

@app.route('/authors', methods=['POST'])
def create_author():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    bio = data.get('bio')
    profile_picture = data.get('profile_picture')

    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO Author (username, email, password, bio, profile_picture)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, email, password, bio, profile_picture))
            conn.commit()
            user_id = cursor.lastrowid
            return jsonify(user_id=user_id, username=username, email=email, bio=bio, profile_picture=profile_picture), 201
        except sqlite3.IntegrityError as e:
            return jsonify(error=str(e)), 400

@app.route('/authors/<int:user_id>', methods=['GET'])
def get_author(user_id):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Author WHERE user_id=?', (user_id,))
        author = cursor.fetchone()
        if author:
            return jsonify(user_id=author[0], username=author[1], email=author[2], bio=author[4], profile_picture=author[5]), 200
        else:
            return jsonify(error="Author not found"), 404

@app.route('/authors/<int:user_id>', methods=['PUT'])
def update_author(user_id):
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    bio = data.get('bio')
    profile_picture = data.get('profile_picture')

    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Author SET username=?, email=?, bio=?, profile_picture=?
            WHERE user_id=?
        ''', (username, email, bio, profile_picture, user_id))
        conn.commit()
        if cursor.rowcount:
            return jsonify(user_id=user_id, username=username, email=email, bio=bio, profile_picture=profile_picture), 200
        else:
            return jsonify(error="Author not found"), 404

@app.route('/authors/<int:user_id>', methods=['DELETE'])
def delete_author(user_id):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Author WHERE user_id=?', (user_id,))
        conn.commit()
        if cursor.rowcount:
            return jsonify(message="Author deleted"), 200
        else:
            return jsonify(error="Author not found"), 404

@app.route('/blogentries', methods=['POST'])
def create_blog_entry():
    data = request.get_json()
    user_id = data.get('user_id')
    title = data.get('title')
    subtitle = data.get('subtitle')
    blurb = data.get('blurb')
    content = data.get('content')
    is_published = data.get('is_published', False)
    time_created = datetime.now()
    time_updated = time_created

    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO BlogEntry (user_id, title, subtitle, blurb, content, time_created, time_updated, is_published)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, title, subtitle, blurb, content, time_created, time_updated, is_published))
        conn.commit()
        post_id = cursor.lastrowid
        return jsonify(post_id=post_id, user_id=user_id, title=title, subtitle=subtitle, blurb=blurb, content=content, is_published=is_published, time_created=time_created), 201

@app.route('/blogentries/<int:post_id>', methods=['GET'])
def get_blog_entry(post_id):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM BlogEntry WHERE post_id=?', (post_id,))
        entry = cursor.fetchone()
        if entry:
            return jsonify(post_id=entry[0], user_id=entry[1], title=entry[2], subtitle=entry[3], blurb=entry[4], content=entry[5], time_created=entry[6], time_updated=entry[7], is_published=entry[8]), 200
        else:
            return jsonify(error="Blog entry not found"), 404

@app.route('/blogentries/<int:post_id>', methods=['PUT'])
def update_blog_entry(post_id):
    data = request.get_json()
    title = data.get('title')
    subtitle = data.get('subtitle')
    blurb = data.get('blurb')
    content = data.get('content')
    is_published = data.get('is_published', False)
    time_updated = datetime.now()

    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE BlogEntry SET title=?, subtitle=?, blurb=?, content=?, time_updated=?, is_published=?
            WHERE post_id=?
        ''', (title, subtitle, blurb, content, time_updated, is_published, post_id))
        conn.commit()
        if cursor.rowcount:
            return jsonify(post_id=post_id, title=title, subtitle=subtitle, blurb=blurb, content=content, time_updated=time_updated, is_published=is_published), 200
        else:
            return jsonify(error="Blog entry not found"), 404

@app.route('/blogentries/<int:post_id>', methods=['DELETE'])
def delete_blog_entry(post_id):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM BlogEntry WHERE post_id=?', (post_id,))
        conn.commit()
        if cursor.rowcount:
            return jsonify(message="Blog entry deleted"), 200
        else:
            return jsonify(error="Blog entry not found"), 404

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)