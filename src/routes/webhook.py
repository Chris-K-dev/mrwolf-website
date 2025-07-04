import os
import requests
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

webhook_bp = Blueprint('webhook', __name__)

# Webhook URLs (stored securely on backend)
FORM_WEBHOOK_URL = "https://mrmrwolf.app.n8n.cloud/webhook/13e7c66f-bf12-49cb-9dbd-39f1cc1b8cf7"
CHAT_WEBHOOK_URL = "https://mrmrwolf.app.n8n.cloud/webhook/16f5e982-0c43-49c8-afba-4c9ac5be243f"

@webhook_bp.route('/form-submit', methods=['POST'])
@cross_origin()
def handle_form_submission():
    """
    Securely handle form submissions by forwarding to the webhook
    """
    try:
        # Get form data from request
        form_data = request.get_json()
        
        if not form_data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['firstName', 'lastName', 'email', 'company']
        for field in required_fields:
            if not form_data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Forward to webhook
        response = requests.post(
            FORM_WEBHOOK_URL,
            json=form_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            return jsonify({'success': True, 'message': 'Form submitted successfully'}), 200
        else:
            return jsonify({'error': 'Failed to submit form'}), 500
            
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Network error occurred'}), 500
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500

@webhook_bp.route('/chat-message', methods=['POST'])
@cross_origin()
def handle_chat_message():
    """
    Securely handle chat messages by forwarding to the webhook
    """
    try:
        # Get chat data from request
        chat_data = request.get_json()
        
        if not chat_data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        if not chat_data.get('message'):
            return jsonify({'error': 'Missing message'}), 400
        
        # Forward to webhook
        response = requests.post(
            CHAT_WEBHOOK_URL,
            json=chat_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            return jsonify({'success': True, 'response': response.json()}), 200
        else:
            return jsonify({'error': 'Failed to process chat message'}), 500
            
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Network error occurred'}), 500
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500

