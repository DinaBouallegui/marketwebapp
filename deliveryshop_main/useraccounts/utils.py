from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
#this file contains any helper function we need to run my features
 
#this function will help to detect the user
def detectUser(user):
    if user.role == 1:
        redirectUrl = 'vendorDashboard'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'customerDashboard'
        return redirectUrl
    elif user.role == None and user.is_superadmin: 
        redirectUrl = '/admin'
        return redirectUrl
    

#this helper function will help to send verification email

def send_verification_email(request,user):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    mail_subject ='Please activate your account' 
    # this is going to be the body of the email:
    message = render_to_string('useraccounts/emails/account_verfication_email.html', {
# pass the values that I want to send to the file account_verfication_email.html
    'user':user,
    'domain': current_site,
    #the encoded version of user's primary key
    # The user primary key needs to be encoded before its send the the email
    #encoding:
    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
    'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    # EmailMessage used  to send the email
    mail = EmailMessage(mail_subject,message, from_email, to=[to_email])
    mail.send()

def send_notification(mail_subject, mail_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template, context)
    if (isinstance(context['to_email'],str)):
        to_email = []
        to_email.append(context['to_email'])
    else:
        to_email = context['to_email']
    mail = EmailMessage(mail_subject, message, from_email, to=to_email)
    mail.send()