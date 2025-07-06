from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os
import time

app = Flask(__name__)
CORS(app)

# Database connection with retry logic
def get_db_connection():
    max_retries = 5
    for i in range(max_retries):
        try:
            conn = psycopg2.connect(
                host=os.environ.get('DB_HOST', 'localhost'),
                user=os.environ.get('DB_USER', 'devtedsuser'),
                password=os.environ.get('DB_PASSWORD', 'devtedspass'),
                database=os.environ.get('DB_NAME', 'quotevault'),
                port=os.environ.get('DB_PORT', '5432')
            )
            return conn
        except psycopg2.OperationalError as e:
            if i < max_retries - 1:
                print(f"Database connection failed, retrying in 5 seconds... ({i+1}/{max_retries})")
                time.sleep(5)
            else:
                print(f"Failed to connect to database after {max_retries} attempts")
                raise e

@app.route('/api/quotes', methods=['GET'])
def get_quotes():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, quote FROM quotes ORDER BY id DESC")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify([{"id": r[0], "quote": r[1]} for r in rows])
    except Exception as e:
        print(f"Error fetching quotes: {e}")
        return jsonify({"error": "Failed to fetch quotes"}), 500

@app.route('/api/quotes', methods=['POST'])
def add_quote():
    try:
        data = request.get_json()
        if not data or 'quote' not in data:
            return jsonify({"error": "Quote text is required"}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO quotes (quote) VALUES (%s)", (data['quote'],))
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Quote added successfully!"}), 201
    except Exception as e:
        print(f"Error adding quote: {e}")
        return jsonify({"error": "Failed to add quote"}), 500

@app.route('/api/quotes/<int:id>', methods=['DELETE'])
def delete_quote(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM quotes WHERE id=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Quote deleted successfully!"})
    except Exception as e:
        print(f"Error deleting quote: {e}")
        return jsonify({"error": "Failed to delete quote"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)