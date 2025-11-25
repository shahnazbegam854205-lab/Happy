from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/api/vehicle/<vehicle_number>')
def get_vehicle_info(vehicle_number):
    try:
        print(f"Fetching data for vehicle: {vehicle_number}")
        
        # NEW API CALL
        response = requests.get(f'https://vechileinfoapi.anshppt19.workers.dev/api/rc?number={vehicle_number}')
        
        if response.status_code == 200:
            data = response.json()
            print("Data fetched successfully from NEW API")
            
            # Remove credit and developer fields from response
            if 'credit' in data:
                del data['credit']
            if 'developer' in data:
                del data['developer']
            
            return jsonify({
                'success': True,
                'data': data
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to fetch vehicle data'
            }), 500
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
