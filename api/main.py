from flask import Flask, request, jsonify
from flask import Limiter
from flask import get_remote_address
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)
limiter = Limiter(app, key_func=get_remote_address, default_limits=["1 per 10 minutes"])

# CONFIG - Use environment variables for safety
EMAIL_HOST = os.getenv("CONTACT_SMTP_HOST", "smtp.example.com")
EMAIL_PORT = int(os.getenv("CONTACT_SMTP_PORT", "587"))
EMAIL_ADDRESS = os.getenv("CONTACT_EMAIL_ADDRESS", "your@email.com")
EMAIL_PASSWORD = os.getenv("CONTACT_EMAIL_PASSWORD", "your_password")
EMAIL_RECEIVER = os.getenv("CONTACT_RECEIVER", "you@yourdomain.com")

@app.route("/api/contact", methods=["POST"])
@limiter.limit("1 per 10 minutes")
def contact():
    try:
        name = request.form["name"]
        email = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]

        if not all([name, email, subject, message]):
            return jsonify(success=False, message="All fields are required."), 400

        email_msg = EmailMessage()
        email_msg["From"] = EMAIL_ADDRESS
        email_msg["To"] = EMAIL_RECEIVER
        email_msg["Subject"] = f"[AJServers Contact] {subject}"

        body = f"""
        You have a new contact message from ajholzer.net:

        Name: {name}
        Email: {email}
        Subject: {subject}
        Message:
        {message}
        """
        email_msg.set_content(body)

        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(email_msg)

        return jsonify(success=True, message="Message sent successfully!")

    except Exception as e:
        print("Email error:", e)
        return jsonify(success=False, message="Server error, please try later."), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
