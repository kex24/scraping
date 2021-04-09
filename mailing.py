# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 15:36:56 2021

@author: msevc
"""

import smtplib
import ssl
import os


def send_mail(address, subject, body):
    # Email credentials
    EMAIL_USER = os.environ['EMAIL_USER']
    EMAIL_PWD = os.environ['EMAIL_PWD']
    
    # Create a secure SSL context
    context = ssl.create_default_context()
    
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls(context=context)
        smtp.ehlo()
        
        smtp.login(EMAIL_USER, EMAIL_PWD)
        
        msg = f'Subject: {subject}\n\n{body}'
        
        smtp.sendmail(EMAIL_USER, address, msg)


if __name__ == '__main__':
    address = 'mrt.sevcik@gmail.com'
    subject = 'This test'
    body = 'Does it work?'
    
    send_mail(address, subject, body)