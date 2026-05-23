import os
from twilio.rest import Client
import logging

logger = logging.getLogger(__name__)

# Fetch environment variables for Twilio (falling back to empty for development mock)
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER', '+1234567890')

def send_emergency_sms(phone_number, message_body):
    """
    Sends an SMS using Twilio.
    If credentials are not set, it mocks the send by logging to console.
    """
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        print(f"\n[MOCK TWILIO SMS] To: {phone_number} | Message: {message_body}\n")
        return True
    
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        return True
    except Exception as e:
        logger.error(f"Failed to send Twilio SMS: {e}")
        return False
