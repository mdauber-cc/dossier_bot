from flask import Flask, jsonify
from src.services.calendar import log_todays_events

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify(status="ok")

@app.route('/run', methods=['POST', 'GET'])
def run():
    count = log_todays_events()
    return jsonify(events_logged=count)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)