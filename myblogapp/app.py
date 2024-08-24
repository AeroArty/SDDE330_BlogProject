from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime
import bloglog as bloglog

app = Flask(__name__)
db_name = 'myblog.db'

def init_db():
    
    pass

def write_log(response, msg):
    bloglogger = bloglog.BlogLog()
    bloglogger.log_api_call(request.method, request.path, response, msg)

@app.route('/')
def index():
    write_log(200, "index called")
    return render_template('index.html')

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
            write_log(201, "create_author")
            return jsonify(user_id=user_id, username=username, email=email, bio=bio, profile_picture=profile_picture), 201
        except sqlite3.IntegrityError as e:
            write_log(400, "create author")
            return jsonify(error=str(e)), 400

@app.route('/authors/<int:user_id>', methods=['GET'])
def get_author(user_id):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Author WHERE user_id=?', (user_id,))
        author = cursor.fetchone()
        if author:
            write_log(200, "get_author({user_id})")
            return jsonify(user_id=author[0], username=author[1], email=author[2], bio=author[4], profile_picture=author[5]), 200
        else:
            write_log(404, "get_author({user_id})")
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
            write_log(200, "update_author({user_id})")
            return jsonify(user_id=user_id, username=username, email=email, bio=bio, profile_picture=profile_picture), 200
        else:
            write_log(404, "update_author({user_id})")
            return jsonify(error="Author not found"), 404

@app.route('/authors/<int:user_id>', methods=['DELETE'])
def delete_author(user_id):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Author WHERE user_id=?', (user_id,))
        conn.commit()
        if cursor.rowcount:
            write_log(200, "delete_author({user_id})")
            return jsonify(message="Author deleted"), 200
        else:
            write_log(404, "delete_author({user_id})")
            return jsonify(error="Author not found"), 404

@app.route('/api/blogentries/', methods=['POST'])
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
        write_log(201, "create_blog_entry())")
        return jsonify(post_id=post_id, user_id=user_id, title=title, subtitle=subtitle, blurb=blurb, content=content, is_published=is_published, time_created=time_created), 201

@app.route('/api/blogentries/<int:post_id>', methods=['GET'])
def get_blog_entry(post_id):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM BlogEntry WHERE post_id=?', (post_id,))
        entry = cursor.fetchone()
        if entry:
            write_log(200, "get_blog_entry({post_id}))")
            return jsonify(post_id=entry[0], user_id=entry[1], title=entry[2], subtitle=entry[3], blurb=entry[4], content=entry[5], time_created=entry[6], time_updated=entry[7], is_published=entry[8]), 200
        else:
            write_log(404, "create_blog_entry({post_id}))")
            return jsonify(error="Blog entry not found"), 404
        
@app.route('/api/blogentries/all', methods=['GET'])
def get_blog_entries():
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        
        # Query to get all blog entries
        cursor.execute("SELECT * FROM BlogEntry")
        rows = cursor.fetchall()
        
        # Convert the query result to a list of dictionaries
        blog_entries = []
        for row in rows:
            blog_entry = {
                'post_id': row[0],
                'user_id': row[1],
                'title': row[2],
                'subtitle': row[3],
                'blurb': row[4],
                'content': row[5],
                'time_created': row[6],
                'time_updated': row[7],
                'is_published': row[8]
            }
            blog_entries.append(blog_entry)
        
        # Return the data as a JSON response
        write_log(999, "get_blog_entries()")
        return jsonify(blog_entries)

@app.route('/api/blogentries/<int:post_id>', methods=['PUT'])
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
            write_log(200, "update_blog_entry({post_id})")
            return jsonify(post_id=post_id, title=title, subtitle=subtitle, blurb=blurb, content=content, time_updated=time_updated, is_published=is_published), 200
        else:
            write_log(404, "update_blog_entry({post_id})")
            return jsonify(error="Blog entry not found"), 404

@app.route('/api/blogentries/<int:post_id>', methods=['DELETE'])
def delete_blog_entry(post_id):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM BlogEntry WHERE post_id=?', (post_id,))
        conn.commit()
        if cursor.rowcount:
            write_log(200, "delete_blog_entry({post_id})")
            return jsonify(message="Blog entry deleted"), 200
        else:
            write_log(404, "delete_blog_entry({post_id})")
            return jsonify(error="Blog entry not found"), 404

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8080)
