from flask import request, jsonify
from app import app, supabase
from app.models import Contact

# CREATE
@app.route('/contacts', methods=['POST'])
def create_contact():
    data = request.get_json()
    try:
        # Execute the query
        response = supabase.table('contacts').insert({
            'name': data['name'],
            'email': data['email'],
            'phone': data.get('phone')
        }).execute()
        
        # Handle response based on Supabase client behavior
        if hasattr(response, 'data') and response.data:
            return jsonify(response.data[0]), 201
        elif hasattr(response, 'json'):
            # Some versions might have json() method
            return jsonify(response.json()[0]), 201
        else:
            # Last resort - convert to string and parse
            import json
            response_str = str(response)
            if "data" in response_str:
                # Try to extract data from string representation
                start = response_str.find("data=") + 5
                end = response_str.find(")", start)
                data_str = response_str[start:end]
                return jsonify(json.loads(data_str)[0]), 201
            else:
                return jsonify({'error': 'Could not parse response'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# READ ALL
@app.route('/contacts', methods=['GET'])
def get_contacts():
    try:
        response = supabase.table('contacts').select('*').execute()
        return jsonify(response['data']), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# READ ONE
@app.route('/contacts/<int:contact_id>', methods=['GET'])
def get_contact(contact_id):
    try:
        response = supabase.table('contacts').select('*').eq('id', contact_id).execute()
        if response['data']:
            return jsonify(response['data'][0]), 200
        return jsonify({'error': 'Contact not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# UPDATE
@app.route('/contacts/<int:contact_id>', methods=['PUT'])
def update_contact(contact_id):
    data = request.get_json()
    try:
        response = supabase.table('contacts').update({
            'name': data.get('name'),
            'email': data.get('email'),
            'phone': data.get('phone')
        }).eq('id', contact_id).execute()
        if response['data']:
            return jsonify(response['data'][0]), 200
        return jsonify({'error': 'Contact not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# DELETE
@app.route('/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    try:
        response = supabase.table('contacts').delete().eq('id', contact_id).execute()
        if response['data']:
            return jsonify({'message': 'Contact deleted'}), 200
        return jsonify({'error': 'Contact not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500