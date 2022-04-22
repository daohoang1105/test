import smtplib
from email.message import EmailMessage

from matplotlib.pyplot import text

def MyFunction(q,w,e,r,t,y,u,i,o,p):
    app_pass = "bmkeowkytzcizkio"
    host_user = "sungrow.service.bot@gmail.com"
    rec_user = "dvh49325@gmail.com"

    texttest = q +" "+ w +" "+ e +" "+ r +" "+ t +" "+ y +" "+ u +" "+ i +" "+ o +" "+ p

    smtp = smtplib.SMTP_SSL('smtp.gmail.com',465)
    smtp.login(host_user, app_pass)

    msg = EmailMessage()
    msg['Subject'] = "Sungrow Inverter " + q + ': ' + w
    msg['From'] = host_user
    msg['To'] = rec_user
    msg.add_alternative(texttest, subtype="html")

    smtp.send_message(msg)

def function2(q,w,e,r,t,y,u,i,o,p):
    print(q,w,e,r,t,y,u,i,o,p)

def functionTest():
    print('=========================================DONE===============================================')

if __name__ == 'main':
    pass
