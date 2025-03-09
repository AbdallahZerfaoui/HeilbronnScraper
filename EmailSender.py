from imports import *
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import os
# from config import SENDER, PASSWORD, STMP_SERVER, STMP_PORT

class EmailSender:
    def __init__(self, sender_email = SENDER, sender_password = PASSWORD):
        """
        Initialize the GmailSender with the sender's email and password.

        :param sender_email: The Gmail address of the sender.
        :param sender_password: The app password or Gmail password of the sender.
        """
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = STMP_SERVER
        self.smtp_port = STMP_PORT  # Port for TLS

    def send_email(self, recipient_email, subject, body, is_html=False):
        """
        Send an email to the specified recipient.

        :param recipient_email: The email address of the recipient.
        :param subject: The subject of the email.
        :param body: The body/content of the email.
        :param is_html: If True, the body is treated as HTML. Default is False (plain text).
        :return: True if the email was sent successfully, False otherwise.
        """
        try:
            # Create the email
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject

            # Attach the body (plain text or HTML)
            if is_html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))

            # Connect to the SMTP server
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Upgrade the connection to secure
                server.login(self.sender_email, self.sender_password)  # Log in to the server
                server.sendmail(self.sender_email, 
                                recipient_email,
                                msg.as_string())  # Send the email

            print(f"Email sent successfully to {recipient_email}")
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False