import os
import base64
import email
import imaplib
import pyttsx3

# text to speech conversion code
text_to_speech = pyttsx3.init()
voices = text_to_speech.getProperty('voices')
for voice in voices:
    text_to_speech.setProperty('voice', voice.id)
voice_rate = 120
text_to_speech.setProperty('rate', voice_rate)

# attachment dir code
detach_dir = '.'
if 'attachments' not in os.listdir(detach_dir):
    os.mkdir('attachments')
# login credentials

username = "iamdummy363@gmail.com"
password = "iuhyexjdakxkpewx"
gmail_host = 'imap.gmail.com'

mail = imaplib.IMAP4_SSL(gmail_host)

# login with exception
try:
    mail.login(username, password)
    print("Logged in as %r !" % username)
except imaplib.IMAP4.error:
    print("Login failed.")

# select inbox and search for unread emails
mail.select("INBOX")
typ, selected_mails = mail.search(None, 'UNSEEN')

x = len(selected_mails[0].split())
print("Total unread mails: ", x)
text_to_speech.say("Total unread emails: ")
text_to_speech.say(x)

# CODE FOR READING THE MAILS
for num in selected_mails[0].split():
    typ, data = mail.fetch(num, '(RFC822)')
    typ, bytes_data = data[0]
    # converting the byte data to message
    email_message = email.message_from_bytes(bytes_data)
    print("--------------- S T A R T ---------------")
    # reading the from address
    text_to_speech.say("The mail is from ")
    text_to_speech.say(email_message["from"])
    # reading the subject
    text_to_speech.say("The subject is ")
    text_to_speech.say(email_message["subject"])
    # reading the body
    text_to_speech.say("The body of mail is: ")
    # accessed data
    print("From: ", email_message["from"])
    print("To: ", email_message["to"])
    print("Date: ", email_message["date"])
    print("Subject: ", email_message["subject"])

    for part in email_message.walk():
        if part.get_content_type() == "text/plain" or part.get_content_type() == "text/html":
            message = part.get_payload(decode=True)
            text_to_speech.say(message.decode())
            print("Body: \n", message.decode())
            text_to_speech.runAndWait()
            print("-------------- E N D ---------------")
            break

# CODE FOR DOWNLOADING THE ATTACHMENTS
try:
    for part in email_message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        file_name = part.get_filename()
        if bool(file_name):
            file_path = os.path.join(detach_dir, 'attachments', file_name)
            if not os.path.isfile(file_path):
                print(file_name)
                fp = open(file_path, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
    mail.close()
    mail.logout()
except:
    print("Not able to download all attachments")
