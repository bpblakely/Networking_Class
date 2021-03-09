import smtplib, ssl
from getpass import getpass
import time											#for waits, testing

from email import *
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText				#supports document attachments

sslPort = 465 										#SMTP SSL - Outgoing
sender_email = input("Type in your email: ")
sender_password = getpass()	
recipient_email = "nholcom@bgsu.edu"

#customize your email? if not, you're gonna get a stupid meme in your inbox
x = ""
while x.lower() != "y" or x.lower() != "n":
	x=input("Customize email fields? y/n: ")

	if x.lower() == "y":
		print("Customize each field, then press enter when finished.\n")
		subject = input("Subject: ")
		body = input("Body: ")
		filename = input("Attachment file name (leave blank if none): ")
		break

	elif x.lower() == "n":
		subject = "Inquiry - Gluten Free Bread Bank"
		body = "Welcome to the bread bank."
		filename = "breadbank.mp4"
		break

	else:
		pass		

message = MIMEMultipart()
message["From"] = sender_email
message["To"] = recipient_email
message["Subject"] = subject
message.attach(MIMEText(body,"plain"))

with open(filename, "rb") as attachment:
	p = MIMEBase("applciation","octet-stream")
	p.set_payload(attachment.read())

encoders.encode_base64(p)

p.add_header("Content-Disposition", f"attachment; filename = {filename}")

message.attach(p)
txt = message.as_string()

#==================================== begin SMTP / SSL connection ==========================================#

context = ssl.create_default_context()				#returns a new SSLContext obj w/ default settings;
													#more info at t.ly/JlqG

with smtplib.SMTP_SSL("smtp.gmail.com", sslPort, context=context) as server:
	server.login(sender_email,sender_password)

	print("Login sucessful.")
	server.sendmail(sender_email,recipient_email,txt)
