from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    """Main Side - Test endpoint """
    return jsonify({
        'message': 'Hello in CSV Importer Application!',
        'status': 'running',
        'version': '1.0.0'
    })

@app.route('/health')
def health():
    """Endpoint to check application status"""
    return jsonify({
        'status': 'healthy',
        'service': 'csv-importer'
    }), 200

@app.route('/api/info')
def api_info():
    """Info about available endpoints"""
    return jsonify({
        'endpoints': [
            {'path': '/', 'method': 'GET', 'description': 'Main Site'},
            {'path': '/health', 'method': 'GET', 'description': 'Application Status'},
            {'path': '/api/info', 'method': 'GET', 'description': 'Info About API'}
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
