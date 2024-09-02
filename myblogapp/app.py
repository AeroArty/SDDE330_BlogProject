from flask import Flask, request, jsonify, render_template
import bloglog as bloglog
import database as db

app = Flask(__name__)

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
    user_id = db.create_author(data.get('username'), data.get('email'), data.get('password'), data.get('bio'), data.get('profile_picture'))
    if user_id:
        write_log(201, "create_author")
        return jsonify(user_id=user_id, **data), 201
    else:
        write_log(400, "create author")
        return jsonify(error="Error creating new author"), 400

@app.route('/authors/<int:user_id>', methods=['GET'])
def get_author(user_id):
    author = db.get_author(user_id)
    if author:
        write_log(200, f"get_author({user_id})")
        return jsonify(user_id=author[0], username=author[1], email=author[2], bio=author[4], profile_picture=author[5]), 200
    else:
        write_log(404, f"get_author({user_id})")
        return jsonify(error="Author not found"), 404

@app.route('/authors/<int:user_id>', methods=['PUT'])
def update_author(user_id):
    data = request.get_json()
    rowcount = db.update_author(user_id, data.get('username'), data.get('email'), data.get('bio'), data.get('profile_picture'))
    if rowcount:
        write_log(200, f"update_author({user_id})")
        return jsonify(user_id=user_id, **data), 200
    else:
        write_log(404, f"update_author({user_id})")
        return jsonify(error="Author not found"), 404

@app.route('/authors/<int:user_id>', methods=['DELETE'])
def delete_author(user_id):
    rowcount = db.delete_author(user_id)
    if rowcount:
        write_log(200, f"delete_author({user_id})")
        return jsonify(message="Author deleted"), 200
    else:
        write_log(404, f"delete_author({user_id})")
        return jsonify(error="Author not found"), 404

@app.route('/api/blogentries/', methods=['POST'])
def create_blog_entry():
    data = request.get_json()
    post_id, time_created = db.create_blog_entry(data.get('user_id'), data.get('title'), data.get('subtitle'), data.get('blurb'), data.get('content'), data.get('is_published', False))
    write_log(201, "create_blog_entry()")
    return jsonify(post_id=post_id, time_created=time_created, **data), 201

@app.route('/api/blogentries/<int:post_id>', methods=['GET'])
def get_blog_entry(post_id):
    entry = db.get_blog_entry(post_id)
    if entry:
        write_log(200, f"get_blog_entry({post_id})")
        return jsonify(post_id=entry[0], user_id=entry[1], title=entry[2], subtitle=entry[3], blurb=entry[4], content=entry[5], time_created=entry[6], time_updated=entry[7], is_published=entry[8]), 200
    else:
        write_log(404, f"get_blog_entry({post_id})")
        return jsonify(error="Blog entry not found"), 404

@app.route('/api/blogentries/all', methods=['GET'])
def get_blog_entries():
    rows = db.get_blog_entries()
    blog_entries = [
        {
            'post_id': row[0],
            'user_id': row[1],
            'title': row[2],
            'subtitle': row[3],
            'blurb': row[4],
            'content': row[5],
            'time_created': row[6],
            'time_updated': row[7],
            'is_published': row[8]
        } for row in rows
    ]
    write_log(200, "get_blog_entries()")
    return jsonify(blog_entries)

@app.route('/api/blogentries/<int:post_id>', methods=['PUT'])
def update_blog_entry(post_id):
    data = request.get_json()
    rowcount, time_updated = db.update_blog_entry(post_id, data.get('title'), data.get('subtitle'), data.get('blurb'), data.get('content'), data.get('is_published', False))
    if rowcount:
        write_log(200, f"update_blog_entry({post_id})")
        return jsonify(post_id=post_id, time_updated=time_updated, **data), 200
    else:
        write_log(404, f"update_blog_entry({post_id})")
        return jsonify(error="Blog entry not found"), 404

@app.route('/api/blogentries/<int:post_id>', methods=['DELETE'])
def delete_blog_entry(post_id):
    rowcount = db.delete_blog_entry(post_id)
    if rowcount:
        write_log(200, f"delete_blog_entry({post_id})")
        return jsonify(message="Blog entry deleted"), 200
    else:
        write_log(404, f"delete_blog_entry({post_id})")
        return jsonify(error="Blog entry not found"), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
