from flask import Flask, request, jsonify
import base64
import json

app = Flask(__name__)

def zIX(hh):
    try:
        parts = hh.split('.')
        if len(parts) < 2:
            return None
        payload_base64 = parts[1]
        padding = 4 - len(payload_base64) % 4
        if padding != 4:
            payload_base64 += '=' * padding
        payload_json = base64.b64decode(payload_base64).decode('utf-8')
        payload = json.loads(payload_json)    
        return {
            "a": payload.get('access_token'),
            "o": payload.get('user', {}).get('open_id')
        }
    except Exception:
        return None

@app.route('/acces_token', methods=['GET'])
def decode_jwt():
    jwt_token = request.args.get('jwt')
    
    if not jwt_token:
        return "Error: Missing 'jwt' parameter", 400
        
    result = zIX(jwt_token)
    
    if not result or not result['a']:
        return "Error: Invalid JWT token structure", 400
        
    return f"acces token --> {result['a']}\nopen id --> {result['o']}"

if __name__ == '__main__':
    app.run()