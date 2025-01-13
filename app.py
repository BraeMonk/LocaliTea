from flask import Flask, request, jsonify, render_template
import json
import os
from dotenv import load_dotenv  # changed the import to match the package name
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  # Update with your frontend's origin

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load JSON structure (if needed)
try:
    with open('data.json') as json_file:
        data_structure = json.load(json_file)
except FileNotFoundError:
    data_structure = {}

@app.route('/')
def index():
    return render_template('/templates/index.html')

@app.route('/send-verification-email', methods=['POST'])
def send_verification_email():
    data = request.json
    username = data.get('username')
    email = data.get('email')

    # Simulate sending email for this example
    if username and email:
        # Send actual email
        try:
            send_email(email, username)
            return jsonify({'message': f'Verification email sent to {email}'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid input'}), 400

def send_email(to_email, username):
    from_email = os.getenv('EMAIL_ADDRESS')
    email_password = os.getenv('EMAIL_PASSWORD')

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = 'Email Verification'

    body = f'Hello {username},\n\nPlease verify your email address by clicking the link below.\n\nThank you!'
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(from_email, email_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)

@app.route('/verify-email', methods=['GET'])
def verify_email():
    username = request.args.get('username')
    if username:
        # Simulate email verification for this example
        return jsonify({'message': f'Email verified for user: {username}'})
    else:
        return jsonify({'error': 'Invalid input'}), 400

if __name__ == '__main__':
    app.run(debug=True)
