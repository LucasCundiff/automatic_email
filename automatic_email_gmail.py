import tkinter as tk
from tkinter import filedialog
import threading
import smtplib
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

smtp_server = 'smtp.gmail.com'
smtp_port = 587

def browse_file():
    filename = filedialog.askopenfilename()
    recipient_file_entry.delete(0, tk.END)
    recipient_file_entry.insert(0, filename)

def send_email():
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(email_entry.get(), password_entry.get())

    with open(recipient_file_entry.get(), 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            msg = MIMEMultipart()
            msg['From'] = email_entry.get()
            msg['To'] = row['email']
            msg['Subject'] = subject_entry.get()
            msg.attach(MIMEText(body_text.get("1.0", tk.END).format(name=row['name'], user=sender_name_entry.get()), 'plain'))

            attachment_path = attachment_entry.get()
            if attachment_path:
                attachment = open(attachment_path, 'rb')
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={attachment_path}')
                msg.attach(part)
                attachment.close()

            server.send_message(msg)
            print(f"Sent an email to {row['email']}")
    server.quit()


def schedule_email():
    schedule_time_str = schedule_time_entry.get()
    schedule_time = datetime.strptime(schedule_time_str, "%Y-%m-%d %H:%M")
    delay = (schedule_time - datetime.now()).total_seconds()
    print(delay)
    threading.Timer(delay, send_email).start()

def on_send_click():
    if schedule_check_var.get() == 1:
        schedule_email()
    else:
        send_email()

app = tk.Tk()
app.title("Automated Gmail Tool")

tk.Label(app, text="User Email:").grid(row=0, column=0)
email_entry = tk.Entry(app)
email_entry.grid(row=0, column=1)

tk.Label(app, text="Password:").grid(row=1, column=0)
password_entry = tk.Entry(app, show="*")
password_entry.grid(row=1, column=1)

tk.Label(app, text="Sender Name:").grid(row=2, column=0)
sender_name_entry = tk.Entry(app)
sender_name_entry.grid(row=2, column=1)

tk.Label(app, text="Recipients CSV:").grid(row=3, column=0)
recipient_file_entry = tk.Entry(app)
recipient_file_entry.grid(row=3, column=1)
tk.Button(app, text="Browse", command=browse_file).grid(row=3, column=2)

tk.Label(app, text="Subject:").grid(row=4, column=0)
subject_entry = tk.Entry(app)
subject_entry.grid(row=4, column=1)

tk.Label(app, text="Body:").grid(row=5, column=0)
body_text = tk.Text(app, height=10, width=40)
body_text.grid(row=5, column=1)

tk.Label(app, text="Attachment:").grid(row=6, column=0)
attachment_entry = tk.Entry(app)
attachment_entry.grid(row=6, column=1)
tk.Button(app, text="Browse", command=lambda: attachment_entry.insert(0, filedialog.askopenfilename())).grid(row=6, column=2)

schedule_check_var = tk.IntVar()
schedule_check = tk.Checkbutton(app, text="Scheduled", variable=schedule_check_var)
schedule_check.grid(row=7, column=0)

tk.Label(app, text="Schedule Time (YYYY-MM-DD HH:MM):").grid(row=7, column=1)
schedule_time_entry = tk.Entry(app)
schedule_time_entry.grid(row=7, column=2)

send_button = tk.Button(app, text="Send Email", command=on_send_click)
send_button.grid(row=8, column=1)

app.mainloop()