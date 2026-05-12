from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import requests
import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')

# ═══════════════════════════════════════════════════════════
# CORS HARDENING - Only allow safe origins
# ═══════════════════════════════════════════════════════════
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5000", "http://localhost:3000", "http://127.0.0.1:5000"],
        "methods": ["POST", "GET", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "max_age": 3600,
        "supports_credentials": False
    }
})

# ═══════════════════════════════════════════════════════════
# RATE LIMITING - Prevent DDoS and quota exhaustion
# ═══════════════════════════════════════════════════════════
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# ═══════════════════════════════════════════════════════════
# ENVIRONMENT VARIABLES & CONFIGURATION
# ═══════════════════════════════════════════════════════════
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'
GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama-3.1-8b-instant')
GROQ_MAX_TOKENS = int(os.getenv('GROQ_MAX_TOKENS', '1024'))

# Email configuration
SENDER_EMAIL = os.getenv('ZORQ_SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('ZORQ_SENDER_PASSWORD')
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

# Flask configuration
FLASK_ENV = os.getenv('FLASK_ENV', 'production')
DEBUG_MODE = FLASK_ENV == 'development'

# ═══════════════════════════════════════════════════════════
# VALIDATION & SECURITY FUNCTIONS
# ═══════════════════════════════════════════════════════════

def validate_api_key():
    """Validate that API key is configured"""
    if not GROQ_API_KEY:
        return False, "GROQ_API_KEY not configured. Add it to .env file."
    return True, None

def sanitize_user_input(text):
    """Remove potential prompt injection attack patterns"""
    if not isinstance(text, str):
        return ""
    
    # Patterns that try to override system prompt
    injection_patterns = [
        r'ignore.*instruction',
        r'forget.*system',
        r'override.*prompt',
        r'new.*instruction',
        r'instead.*you.*are',
        r'now.*you.*are',
        r'pretend.*to.*be',
        r'act.*as.*if',
        r'you.*are.*now',
        r'forget.*everything'
    ]
    
    cleaned = text
    for pattern in injection_patterns:
        cleaned = re.sub(pattern, '[REDACTED]', cleaned, flags=re.IGNORECASE)
    
    return cleaned.strip()

def validate_messages(messages):
    """Validate message format and content"""
    if not isinstance(messages, list):
        return False, "Messages must be a list"
    
    if len(messages) == 0:
        return False, "Messages list is empty"
    
    for msg in messages:
        if not isinstance(msg, dict):
            return False, "Each message must be a dict"
        if 'role' not in msg or 'content' not in msg:
            return False, "Each message must have 'role' and 'content'"
        if msg['role'] not in ['system', 'user', 'assistant']:
            return False, "Invalid role. Must be 'system', 'user', or 'assistant'"
        if not isinstance(msg['content'], str):
            return False, "Message content must be a string"
    
    return True, None

@app.route('/')
def home():
    return send_file('loading.html')

@app.route('/api/chat', methods=['POST'])
@limiter.limit("10 per minute")
def chat():
    """Enhanced chat endpoint with security & context windowing"""
    try:
        # Validate API key first
        is_valid, error = validate_api_key()
        if not is_valid:
            return jsonify({'error': error}), 500
        
        data = request.get_json()
        messages = data.get('messages', []) if data else []
        
        # Validate message format
        is_valid, error = validate_messages(messages)
        if not is_valid:
            print(f'[ERROR] Invalid messages: {error}')
            return jsonify({'error': error}), 400
        
        # ═══════════════════════════════════════════════════════════
        # CONTEXT WINDOWING - Keep only last 20 messages for efficiency
        # ═══════════════════════════════════════════════════════════
        system_msg = messages[0]
        conversation = messages[1:]
        
        # Keep only last 20 messages to respect token budget
        if len(conversation) > 20:
            conversation = conversation[-20:]
        
        windowed_messages = [system_msg] + conversation
        
        # Sanitize user input (last message)
        if windowed_messages and windowed_messages[-1].get('role') == 'user':
            windowed_messages[-1]['content'] = sanitize_user_input(
                windowed_messages[-1]['content']
            )
        
        print(f'[CHAT] Messages: {len(messages)} | Windowed: {len(windowed_messages)} | Tokens: ~{len(str(windowed_messages)) // 4}')
        
        # ═══════════════════════════════════════════════════════════
        # OPTIMIZED MODEL PARAMETERS
        # ═══════════════════════════════════════════════════════════
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {GROQ_API_KEY}'
        }
        
        payload = {
            'model': GROQ_MODEL,
            'messages': windowed_messages,
            'max_tokens': GROQ_MAX_TOKENS,
            'temperature': 0.6,           # Lower for consistency
            'top_p': 0.9,                 # Nucleus sampling
            'top_k': 50,                  # Vocabulary constraint
            'repetition_penalty': 1.1    # Prevent repetition
        }
        
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code != 200:
            error_data = response.json() if response.text else {}
            error_msg = error_data.get('error', {}).get('message', f'API error: {response.status_code}')
            print(f'[ERROR] Groq API error: {error_msg}')
            return jsonify({'error': error_msg}), response.status_code
        
        data = response.json()
        reply = data.get('choices', [{}])[0].get('message', {}).get('content', 'No response received.')
        
        return jsonify({
            'reply': reply,
            'metadata': {
                'tokens_input': len(str(windowed_messages)) // 4,
                'timestamp': datetime.now().isoformat(),
                'model': GROQ_MODEL
            }
        })
    
    except requests.exceptions.Timeout:
        print(f'[ERROR] Request timeout')
        return jsonify({'error': 'Request timeout - please try again'}), 504
    except requests.exceptions.RequestException as e:
        print(f'[ERROR] Request error: {str(e)}')
        return jsonify({'error': 'API connection error'}), 500
    except Exception as e:
        print(f'[ERROR] Server error: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/send-welcome-email', methods=['POST'])
@limiter.limit("5 per hour")
def send_welcome_email():
    """Send welcome email to newly registered users"""
    try:
        if not SENDER_EMAIL or not SENDER_PASSWORD:
            print(f'[WARNING] Email not configured - skipping welcome email')
            return jsonify({
                'success': False,
                'message': 'Email service not configured',
                'status': 'skipped'
            }), 200
        
        data = request.get_json()
        
        name = data.get('name', 'User').strip()
        email = data.get('email', '').strip()
        user_id = data.get('userId', '').strip()
        
        if not email or not name:
            return jsonify({'error': 'Name and email are required'}), 400
        
        print(f'[DEBUG] Sending welcome email to {email}')
        
        # Email content with HTML formatting
        subject = '✨ Welcome to ZORQ - Your AI Companion!'
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: 'DM Sans', Arial, sans-serif; background: #0a0a0a; color: #e8e8e8; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; background: #111111; border-radius: 16px; border: 1px solid rgba(245,197,0,0.15); }}
                .header {{ text-align: center; padding: 20px 0; border-bottom: 1px solid rgba(245,197,0,0.15); margin-bottom: 20px; }}
                .logo {{ font-size: 28px; font-weight: 900; color: #f5c500; letter-spacing: 6px; text-shadow: 0 0 16px rgba(245,197,0,0.5); }}
                .content {{ padding: 20px 0; }}
                .greeting {{ font-size: 18px; color: #f5c500; margin-bottom: 10px; font-weight: 700; }}
                .message {{ line-height: 1.6; color: #e8e8e8; margin-bottom: 15px; }}
                .details {{ background: rgba(245,197,0,0.05); border: 1px solid rgba(245,197,0,0.12); border-radius: 12px; padding: 15px; margin: 15px 0; }}
                .detail-item {{ margin: 8px 0; font-size: 14px; }}
                .detail-label {{ color: #f5c500; font-weight: 700; }}
                .footer {{ text-align: center; padding: 20px 0; border-top: 1px solid rgba(245,197,0,0.15); margin-top: 20px; font-size: 12px; color: #666; }}
                .cta-button {{ display: inline-block; margin: 15px 0; padding: 12px 24px; background: #f5c500; color: #0a0a0a; border-radius: 10px; text-decoration: none; font-weight: 700; letter-spacing: 2px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="logo">ZORQ</div>
                    <p style="margin: 8px 0; color: #f5c500; font-size: 12px; letter-spacing: 2px;">AI INTELLIGENCE SYSTEM</p>
                </div>
                
                <div class="content">
                    <div class="greeting">🎉 Welcome to ZORQ, {name}!</div>
                    
                    <div class="message">
                        Congratulations on joining ZORQ! Your account has been successfully created. 
                        You're now ready to experience advanced AI conversations and intelligent assistance.
                    </div>
                    
                    <div class="details">
                        <div class="detail-item">
                            <span class="detail-label">👤 Name:</span> {name}
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">📧 Email:</span> {email}
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">🆔 User ID:</span> {user_id}
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">📅 Join Date:</span> {datetime.now().strftime('%B %d, %Y')}
                        </div>
                    </div>
                    
                    <div class="message">
                        <strong>What you can do:</strong>
                        <ul style="margin: 10px 0; padding-left: 20px;">
                            <li>Chat with ZORQ AI in multiple languages (Tamil, English, etc.)</li>
                            <li>Save and manage your conversations</li>
                            <li>Edit and personalize your profile</li>
                            <li>Get intelligent responses to any question</li>
                        </ul>
                    </div>
                    
                    <div style="text-align: center;">
                        <a href="http://localhost:5000/dashboard.html" class="cta-button">START CHATTING →</a>
                    </div>
                    
                    <div class="message" style="font-size: 13px; color: #999; margin-top: 20px;">
                        If you didn't create this account, please ignore this email.
                    </div>
                </div>
                
                <div class="footer">
                    <p>© 2026 ZORQ AI Intelligence System. All rights reserved.</p>
                    <p>This is an automated message. Please do not reply.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        try:
            # Create email message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = SENDER_EMAIL
            msg['To'] = email
            
            # Attach HTML content
            msg.attach(MIMEText(html_content, 'html'))
            
            # Send email via SMTP
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            server.quit()
            
            print(f'[SUCCESS] Welcome email sent to {email}')
            return jsonify({'success': True, 'message': 'Welcome email sent successfully'}), 200
            
        except smtplib.SMTPAuthenticationError:
            print(f'[ERROR] SMTP authentication failed')
            return jsonify({'error': 'Email service auth failed', 'status': 'skipped'}), 200
        except smtplib.SMTPException as e:
            print(f'[ERROR] SMTP error: {str(e)}')
            return jsonify({'error': 'Email service error', 'status': 'skipped'}), 200
        
    except Exception as e:
        print(f'[ERROR] Email handler error: {str(e)}')
        return jsonify({'error': str(e), 'status': 'skipped'}), 200

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files securely"""
    # Prevent directory traversal attacks
    if '..' in filename:
        return jsonify({'error': 'Invalid request'}), 400
    return send_from_directory('.', filename)

if __name__ == '__main__':
    print('🚀 ZORQ Server Starting...')
    print('═' * 50)
    
    # Check configuration
    if not GROQ_API_KEY:
        print('⚠️  WARNING: GROQ_API_KEY not set!')
        print('📋 Add GROQ_API_KEY to .env file')
    else:
        print('✅ GROQ API Key configured')
    
    print(f'📱 Environment: {FLASK_ENV}')
    print(f'🌐 Server: http://localhost:5000')
    print('═' * 50)
    
    app.run(debug=DEBUG_MODE, host='0.0.0.0', port=5000, threaded=True)


@app.route('/api/send-welcome-email', methods=['POST'])
def send_welcome_email():
    """Send welcome email to newly registered users"""
    try:
        data = request.get_json()
        
        name = data.get('name', 'User').strip()
        email = data.get('email', '').strip()
        user_id = data.get('userId', '').strip()
        
        if not email or not name:
            return jsonify({'error': 'Name and email are required'}), 400
        
        print(f'[DEBUG] Sending welcome email to {email}')
        
        # Email content with HTML formatting
        subject = '✨ Welcome to ZORQ - Your AI Companion!'
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: 'DM Sans', Arial, sans-serif; background: #0a0a0a; color: #e8e8e8; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; background: #111111; border-radius: 16px; border: 1px solid rgba(245,197,0,0.15); }}
                .header {{ text-align: center; padding: 20px 0; border-bottom: 1px solid rgba(245,197,0,0.15); margin-bottom: 20px; }}
                .logo {{ font-size: 28px; font-weight: 900; color: #f5c500; letter-spacing: 6px; text-shadow: 0 0 16px rgba(245,197,0,0.5); }}
                .content {{ padding: 20px 0; }}
                .greeting {{ font-size: 18px; color: #f5c500; margin-bottom: 10px; font-weight: 700; }}
                .message {{ line-height: 1.6; color: #e8e8e8; margin-bottom: 15px; }}
                .details {{ background: rgba(245,197,0,0.05); border: 1px solid rgba(245,197,0,0.12); border-radius: 12px; padding: 15px; margin: 15px 0; }}
                .detail-item {{ margin: 8px 0; font-size: 14px; }}
                .detail-label {{ color: #f5c500; font-weight: 700; }}
                .footer {{ text-align: center; padding: 20px 0; border-top: 1px solid rgba(245,197,0,0.15); margin-top: 20px; font-size: 12px; color: #666; }}
                .cta-button {{ display: inline-block; margin: 15px 0; padding: 12px 24px; background: #f5c500; color: #0a0a0a; border-radius: 10px; text-decoration: none; font-weight: 700; letter-spacing: 2px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="logo">ZORQ</div>
                    <p style="margin: 8px 0; color: #f5c500; font-size: 12px; letter-spacing: 2px;">AI INTELLIGENCE SYSTEM</p>
                </div>
                
                <div class="content">
                    <div class="greeting">🎉 Welcome to ZORQ, {name}!</div>
                    
                    <div class="message">
                        Congratulations on joining ZORQ! Your account has been successfully created. 
                        You're now ready to experience advanced AI conversations and intelligent assistance.
                    </div>
                    
                    <div class="details">
                        <div class="detail-item">
                            <span class="detail-label">👤 Name:</span> {name}
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">📧 Email:</span> {email}
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">🆔 User ID:</span> {user_id}
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">📅 Join Date:</span> {datetime.now().strftime('%B %d, %Y')}
                        </div>
                    </div>
                    
                    <div class="message">
                        <strong>What you can do:</strong>
                        <ul style="margin: 10px 0; padding-left: 20px;">
                            <li>Chat with ZORQ AI in multiple languages (Tamil, English, etc.)</li>
                            <li>Save and manage your conversations</li>
                            <li>Edit and personalize your profile</li>
                            <li>Get intelligent responses to any question</li>
                        </ul>
                    </div>
                    
                    <div style="text-align: center;">
                        <a href="http://localhost:5000/dashboard.html" class="cta-button">START CHATTING →</a>
                    </div>
                    
                    <div class="message" style="font-size: 13px; color: #999; margin-top: 20px;">
                        If you didn't create this account, please ignore this email.
                    </div>
                </div>
                
                <div class="footer">
                    <p>© 2026 ZORQ AI Intelligence System. All rights reserved.</p>
                    <p>This is an automated message. Please do not reply.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        try:
            # Create email message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = SENDER_EMAIL
            msg['To'] = email
            
            # Attach HTML content
            msg.attach(MIMEText(html_content, 'html'))
            
            # Send email via SMTP
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            server.quit()
            
            print(f'[SUCCESS] Welcome email sent to {email}')
            return jsonify({'success': True, 'message': 'Welcome email sent successfully'}), 200
            
        except smtplib.SMTPAuthenticationError:
            print(f'[ERROR] SMTP authentication failed - check email credentials')
            return jsonify({'error': 'Email service not configured', 'status': 'skipped'}), 200
        except smtplib.SMTPException as e:
            print(f'[ERROR] SMTP error: {str(e)}')
            return jsonify({'error': f'Email service error: {str(e)}', 'status': 'skipped'}), 200
        
    except Exception as e:
        print(f'[ERROR] Email error: {str(e)}')
        return jsonify({'error': str(e), 'status': 'skipped'}), 200

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    print('🚀 ZORQ server running on http://localhost:5000')
    print('📁 Open your browser and navigate to http://localhost:5000')
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
