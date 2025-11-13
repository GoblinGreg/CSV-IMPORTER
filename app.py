from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    """Główna strona - endpoint testowy"""
    return jsonify({
        'message': 'Witaj w aplikacji CSV Importer!',
        'status': 'running',
        'version': '1.0.0'
    })

@app.route('/health')
def health():
    """Endpoint do sprawdzania stanu aplikacji"""
    return jsonify({
        'status': 'healthy',
        'service': 'csv-importer'
    }), 200

@app.route('/api/info')
def api_info():
    """Informacje o dostępnych endpointach"""
    return jsonify({
        'endpoints': [
            {'path': '/', 'method': 'GET', 'description': 'Strona główna'},
            {'path': '/health', 'method': 'GET', 'description': 'Status aplikacji'},
            {'path': '/api/info', 'method': 'GET', 'description': 'Informacje o API'}
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
