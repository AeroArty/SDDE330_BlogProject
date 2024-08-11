from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if not name:
        return jsonify({"error": "Name is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO items (name, description) VALUES (?, ?)',
        (name, description)
    )
    conn.commit()
    item_id = cursor.lastrowid
    conn.close()

    return jsonify({"id": item_id, "name": name, "description": description}), 201

@app.route('/items', methods=['GET'])
def get_items():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()

    items_list = [{"id": item["id"], "name": item["name"], "description": item["description"]} for item in items]
    return jsonify(items_list), 200

@app.route('/test', methods=['GET'])
def get_test():

    items_list = ["foo", "bar"]
    return jsonify(items_list), 200



@app.route('/items/<int:id>', methods=['GET'])
def get_item(id):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM items WHERE id = ?', (id,)).fetchone()
    conn.close()

    if item is None:
        return jsonify({"error": "Item not found"}), 404

    return jsonify({"id": item["id"], "name": item["name"], "description": item["description"]}), 200

@app.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE items SET name = ?, description = ? WHERE id = ?',
        (name, description, id)
    )
    conn.commit()
    conn.close()

    return jsonify({"id": id, "name": name, "description": description}), 200

@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM items WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Item deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
