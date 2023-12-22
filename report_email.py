import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import reports
import datetime

title = "Processed Update on " + datetime.datetime.now().strftime("%Y/%m/%d")
dir_nm = "./supplier-data/descriptions/"
flist = os.listdir(dir_nm)

info_list = []
for idx in range(len(flist)):
    with open(dir_nm + flist[idx], 'r') as fp:
        lines = fp.readlines()
        if len(lines) < 3:
            pass
        else:
            for num in range(len(lines)):
                if num == 0:
                    info_list.append(lines[num].strip())
                elif num == 1:
                    info_list.append(lines[num].strip())
    info_list.append(" ")

paragraph = "<br/>".join(info_list)
message = reports.generate(filename="/tmp/processed.pdf",
                 title=title,
                 additional_info=paragraph)

#gmail_smtp = "smtp.gmail.com"
#gmail_port = 465
# smtp = smtplib.SMTP_SSL(gmail_smtp, gmail_port)
my_account = "automation@example.com"
my_password = ""
# smtp.login(my_account, my_password)
to_mail = "study_hard@example.com"

#########
import email.message
import mimetypes
import os.path
import smtplib

def gmail_generate(sender, recipient, subject, body, attachment_path=None):
  """Creates an email with an attachement."""
  # Basic Email formatting
  message = email.message.EmailMessage()
  message["From"] = sender
  message["To"] = recipient
  message["Subject"] = subject
  message.set_content(body)

  # Process the attachment and add it to the email

  if attachment_path:
    attachment_filename = os.path.basename(attachment_path)
    mime_type, _ = mimetypes.guess_type(attachment_path)
    mime_type, mime_subtype = mime_type.split('/', 1)
    with open(attachment_path, 'rb') as ap:
      message.add_attachment(ap.read(),
                           maintype=mime_type,
                           subtype=mime_subtype,
                           filename=attachment_filename)
  else:
    pass

  return message

msg = gmail_generate(sender=my_account, recipient=to_mail,
                     subject="Upload Completed - Online Fruit Store",
                     body="Al fruits are uploaded to our website successfully. \n A detailed list is attatched to this email", 
                     attachment_path="/tmp/processed.pdf")


def send_gmail(message):
  """Sends the message to the configured SMTP server."""
  mail_server = smtplib.SMTP('localhost')
  #mail_server = smtplib.SMTP_SSL(gmail_smtp, gmail_port)
  #mail_server.login(my_account, my_password)
  mail_server.send_message(message)
  mail_server.quit()

send_gmail(msg)