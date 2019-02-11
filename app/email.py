#module that'll handle image logic

from flask_mail import Message
from flask import render_template
from . import mail      #import the mail instance from the application factory module.

def mail_message(subject,template,to,**kwargs):
    sender_email = 'dshege4@gmail.com'

    email = Message(subject, sender=sender_email, recipients=[to])
    email.body= render_template(template + ".txt",**kwargs)
    email.html = render_template(template + ".html",**kwargs)
    mail.send(email)        #use the send method of the mailinstance and pass in the email instance.
