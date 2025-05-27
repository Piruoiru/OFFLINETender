from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import subprocess


load_dotenv()

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        result = subprocess.run(
            ["python", "DataExtractor/main.py"], 
            capture_output=True, 
            text=True, 
        )
        return jsonify({
            "status": "done",
            "output": result.stdout,
            "error": result.stderr
        }), 200
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Timeout durante l'esecuzione di main.py"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)