import smtplib,ssl
from getpass import getpass
import time

# need to set up gmail account to be able to get accessed insecurely
sslPort = 465

sender_email = input('Input your email address: ')
sender_password = getpass()

recepient_email = 'bpbrian@bgsu.edu'

msg = 'temp message'

context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com",sslPort, context = context) as server:
    server.login(sender_email, sender_password)
    print("login successful")
    time.sleep(3)
    server.sendmail(sender_email, recepient_email, msg)