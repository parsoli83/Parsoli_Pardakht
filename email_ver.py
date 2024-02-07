import smtplib
from email.message import *
from random import randint







def email_ver(user_email):
    def random_pass(num = "",depth = 4):
        if depth==0:
            return num
        return random_pass(num+str(randint(1,9)),depth-1)
    
    my_email = "parsoli.pardakht@gmail.com"
    my_pass = "kcks uqmv dbha ytyx"
    password = random_pass()
    msg = EmailMessage()
    msg["to"] = user_email
    msg["from"] = my_email
    msg["subject"] = "Password"
    msg.set_content(password)
    with smtplib.SMTP_SSL("smtp.gmail.com",465) as current:
        current.login(my_email,my_pass)
        current.send_message(msg)
    return password




