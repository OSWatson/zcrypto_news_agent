from flask import Flask, jsonify, send_from_directory
import os

app = Flask(__name__)

MODULES_DIR = 'modules'

@app.route('/module/<filename>')
def get_module(filename):
    try:
        return send_from_directory(MODULES_DIR, filename)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=True) 