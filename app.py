from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
from oauthlib.oauth2 import WebApplicationClient
import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Flask app setup
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.secret_key = os.urandom(24)

# OAuth 2.0 client setup
client_id = os.getenv('GOOGLE_CLIENT_ID')
client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
client = WebApplicationClient(client_id)

# Load JSON structure (if needed)
try:
    with open('data_structure.json') as json_file:
        data_structure = json.load(json_file)
except FileNotFoundError:
    data_structure = {}

# Home route
@app.route('/')
def index():
    if 'user' in session:
        return f'Hello, {session["user"]["name"]}!'
    else:
        return 'Hello, Guest! <a href="/login">Login with Google</a>'

# Google login route
@app.route('/login')
def login():
    google_provider_cfg = requests.get("https://accounts.google.com/.well-known/openid-configuration").json()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

# Google login callback route
@app.route('/login/callback')
def callback():
    code = request.args.get("code")
    google_provider_cfg = requests.get("https://accounts.google.com/.well-known/openid-configuration").json()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(client_id, client_secret),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    userinfo = userinfo_response.json()
    session['user'] = userinfo

    return redirect(url_for('index'))

# Route to send verification email
@app.route('/send-verification-email', methods=['POST'])
def send_verification_email():
    data = request.json
    username = data.get('username')
    email = data.get('email')

    if username and email:
        try:
            send_email(email, username)
            return jsonify({'message': f'Verification email sent to {email}'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid input'}), 400

# Function to send email
def send_email(to_email, username):
    from_email = os.getenv('EMAIL_ADDRESS')
    email_password = os.getenv('EMAIL_PASSWORD')

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = 'Email Verification'

    body = f'Hello {username},\n\n
