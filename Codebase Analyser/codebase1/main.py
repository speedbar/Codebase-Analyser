import smtplib
import schedule
import time
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import requests
from cryptography.fernet import Fernet

# Function to send the Excel file via email
def send_email():
    # Email configuration
    sender_email = 'nabeel.thenutty@johnlewis.co.uk'
    sender_password = 'your_email_password'
    #receiver_email = ["glenn.cox@johnlewis.co.uk","amit.kumbhar@johnlewis.co.uk"]
    receiver_email = "nabeel.thenutty@johnlewis.co.uk"
    # Link to the Excel file
    excel_link = 'https://docs.google.com/spreadsheets/d/1BT63_hTIEVtGBxPxeJl9IvKKgaCwZ_d665Joes15DU4/edit?usp=sharing'

    # Download the Excel file,
    downloaded_file_path = 'Competitor.xlsx'

    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    # msg['To'] = ', '.join(receiver_email)
    msg['To'] = receiver_email
    msg['Subject'] = 'Competitor Analysis Report'
    # Attach Excel file
    attachment = open(downloaded_file_path, 'rb')
    excel_attachment = MIMEApplication(attachment.read(), _subtype="xlsx")
    attachment.close()

    excel_attachment.add_header('Content-Disposition', f'attachment; filename={downloaded_file_path}')
    msg.attach(excel_attachment)

    # Connect to SMTP server and send email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        dec = str(Fernet('egupkHT3QJHG1c5dcPGiWEZaWdH04_uhgyD-8lYNxWM=').decrypt(b'gAAAAABlm-TMnsG_dTs3-JVo9-Un2_7LRHBim8EdZksZg69tdxZqnd4L5ZDeUxOagZEoLZHc58o5F12KVispuhg49ndA0EL2s08ZuHJnTtbIu5LmR0cVlOo='), 'UTF-8')
        server.login(sender_email, dec)
        server.send_message(msg)

    print(f"Email sent at {time.strftime('%Y-%m-%d %H:%M:%S')}")
send_email()
# # Schedule the task to run every week
# schedule.every().week.at("08:00").do(send_email)  # Adjust the time as per your requirement

# # Run the scheduled task
# while True:
#     schedule.run_pending()
#     time.sleep(1)