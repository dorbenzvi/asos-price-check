# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
def sendEmail(alert, newPrice):
    message = Mail(
        from_email='sender@gmail.com',
        to_emails=alert.user_Email,
        subject='Hey! The product '+alert.product_name+' Price has been Dropped!',
        html_content='<strong>Hey! The product '+alert.product_name+' Price has been Dropped from '+str(alert.product_price)+'$ To '+str(newPrice)+'$</strong>')
    try:
        sg = SendGridAPIClient('YOUR_API')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
