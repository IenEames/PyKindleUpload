# All the modules required to find and upload books

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

# Variables used to define sender and recepient emails and gmail credentials

fromaddrs = 'YOUR EMAIL ADDRESS'
toaddrs = 'YOUR KINDLE EMAIL '
subject = 'EMAIL SUBJECT'
username = 'USERNAME'
password = 'PASSWORD'

# Bookdir - path to directory with books

bookdir = "...."


def uploadtokindle():
    
    # Creating a base message
    
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = fromaddrs
    msg['To'] = toaddrs

    # Looking for .mobi files in "bookdir" directory. Filtering redundant copies of the files

    booklist = []
    for file in os.listdir(bookdir):
        if file.endswith(".mobi"):
            if not file.endswith(").mobi"):
                mobi_file = os.path.join(bookdir, file)
                mobi = MIMEApplication(open(mobi_file, "rb").read())
                file_name = mobi_file.replace((str(bookdir) + '\\'), "")
                booklist.append(file_name)
                mobi.add_header('Content-Disposition', 'attachment', filename=file_name)
                msg.attach(mobi)

    # If any .mobi books found - preparing to send a message using variables defined in the beginning

    if len(booklist) >= 1:
        if len(booklist) > 1:
            msgtext = "{} books were sent for upload!".format(len(booklist))
        else:
            msgtext = "Book was sent for upload!"
        print(msgtext)
        msgtext = MIMEText(msgtext, 'plain')
        msg.attach(msgtext)

        # Sending an email with book attachments 

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(username, password)
            server.sendmail(fromaddrs, toaddrs, msg.as_string())
            server.close()

            if len(booklist) > 1:
                print("Successfully uploaded the books!")
            else:
                print("Successfully uploaded the book!")
        except:
            print("Failed to upload!")
    else:
        print("No books found!")

uploadtokindle()
