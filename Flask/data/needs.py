import bcrypt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import string
import secrets
import random


def get_hashed_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())


def check_password_hashed(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password)


def checked_email(email):
    sender = "bratsk.post@yandex.ru"
    password_sender = "post-bratsk2023"

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = email
    msg['Subject'] = 'Код подтверждения почты!'

    alphabet = string.ascii_letters + string.digits
    body = ''.join(secrets.choice(alphabet) for i in range(8))
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    server.login(sender, password_sender)
    server.send_message(msg)
    server.quit()
    return body


def random_avatar():
    avatar_list = ['avatar1.jpg', 'avatar2.png', 'avatar3.jpg', 'avatar4.png', 'avatar5.png', 'avatar6.png']
    return random.choice(avatar_list)


def checked_avatar(avatar):
    return avatar in ['avatar1.jpg', 'avatar2.png', 'avatar3.jpg', 'avatar4.png', 'avatar5.png', 'avatar6.png']


def password_check_regular(passwd):
    SpecialSym = ['$', '@', '#', '%']

    if len(passwd) < 6:
        return 'length should be at least 6'

    if len(passwd) > 20:
        return 'length should be not be greater than 8'

    if not any(char.isdigit() for char in passwd):
        return 'Password should have at least one numeral'

    if not any(char.isupper() for char in passwd):
        return 'Password should have at least one uppercase letter'

    if not any(char.islower() for char in passwd):
        return 'Password should have at least one lowercase letter'

    if not any(char in SpecialSym for char in passwd):
        return 'Password should have at least one of the symbols $@#'
    return 'ok'



