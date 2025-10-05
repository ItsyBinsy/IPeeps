"""
Flask Web Application for IP Information Lookup
Single-page web interface for the IP geolocation application
"""

from flask import Flask, render_template, jsonify, request
from api_client import AbstractAPIClient
from data_processor import DataProcessor
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Initialize API client and data processor
try:
    api_client = AbstractAPIClient()
    data_processor = DataProcessor()
except ValueError as e:
    print(f"Error initializing API client: {e}")
    api_client = None
    data_processor = None


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@app.route('/api/current-ip', methods=['GET'])
def get_current_ip():
    """API endpoint to get current IP information"""
    if not api_client:
        return jsonify({'error': 'API client not initialized. Check your API key.'}), 500

    try:
        raw_data = api_client.get_current_ip_info()

        if raw_data:
            processed_data = data_processor.process_all_data(raw_data)
            if processed_data:
                return jsonify({
                    'success': True,
                    'data': processed_data
                })
            else:
                return jsonify({'error': 'Failed to process API response'}), 500
        else:
            return jsonify({'error': 'Failed to retrieve IP information'}), 500

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


@app.route('/api/lookup-ip', methods=['POST'])
def lookup_ip():
    """API endpoint to lookup specific IP address"""
    if not api_client:
        return jsonify({'error': 'API client not initialized. Check your API key.'}), 500

    try:
        data = request.get_json()
        ip_address = data.get('ip_address', '').strip()

        if not ip_address:
            return jsonify({'error': 'No IP address provided'}), 400

        raw_data = api_client.get_specific_ip_info(ip_address)

        if raw_data:
            processed_data = data_processor.process_all_data(raw_data)
            if processed_data:
                return jsonify({
                    'success': True,
                    'data': processed_data
                })
            else:
                return jsonify({'error': 'Failed to process API response'}), 500
        else:
            return jsonify({'error': f'Failed to retrieve information for {ip_address}'}), 500

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


@app.route('/api/test-connection', methods=['GET'])
def test_connection():
    """API endpoint to test API connection"""
    if not api_client:
        return jsonify({'error': 'API client not initialized. Check your API key.'}), 500

    try:
        success = api_client.test_connection()
        if success:
            return jsonify({
                'success': True,
                'message': 'API connection successful!'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'API connection failed'
            }), 500

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)