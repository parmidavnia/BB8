import jwt

from user.models import *


def create_admin():
    first_name = input('Enter first name: ')
    last_name = input('Enter last name: ')
    email = input('Enter Email: ')
    password = ''
    confirm_password = ''
    while password is None or password == '' or password != confirm_password:
        password = input('Enter password: ')
        confirm_password = input('Enter confirm: ')
    token = jwt.encode({'firstName': first_name, 'lastName': last_name, 'email': email}, 'SECRET', algorithm='HS256')
    admin = User(firstName=first_name, lastName=last_name, email=email, password=password, token=token, role='ADMIN')
    admin.save()

    print('Your token is:\n', str(token, encoding='utf-8'))


create_admin()