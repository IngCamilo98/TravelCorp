from dotenv import load_dotenv

load_dotenv()  # take environment variables

from utils.email import send_email

send_email("...", "Test Email", "This is a test email sent from the script.")