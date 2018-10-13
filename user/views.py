import hashlib
import json, jwt
import re

from django.core.validators import validate_email
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from tagger.models import SentenceHistory
from user.models import User


def validateEmail( email ):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False


def authorization_and_get_user(request, userId):
    auth_token = request.META.get('HTTP_AUTH', None)
    users = User.objects.filter(token=auth_token)
    if users is None or len(users) == 0:
        return JsonResponse({
            'result': 'ERR',
            'error': {
                'key': 'AUTHENTICATION_ERROR'
            }
        }), None

    user = users[0]

    if user['role'] != 'ADMIN' and str(user['id']) != userId:
        return JsonResponse({
            'result': 'ERR',
            'error': {
                'key': 'AUTHORIZATION_ERROR'
            }
        }), user

    return None, user

@csrf_exempt
def register(request):
    if request.method == 'POST':
        body = json.loads(request.body)

        firstName = body.get('firstName', None)
        lastName = body.get('lastName', None)
        email = body.get('email', None)
        password = body.get('password', None)
        confirmPassword = body.get('confirmPassword', None)


        if re.search('[A-Z]', password) != None and re.search('[0-9]', password) != None and re.search('[^A-Za-z0-9]', password) != None:

            if password != confirmPassword:
                return JsonResponse(
                    {
                        'result': 'ERR',
                        'error': {
                            'key': 'PASSWORD_AND_CONFIRM_DOES_NOT_MATCH'
                        }
                    }
                )

        else:
            return JsonResponse({
                'result' : 'ERR',
                'error' : {
                    'key' : 'PASSWORD_SHOULD_CONTAIN_BOTH_NUMBERS_AND_CHARACTERS'
                }
            })



        if validateEmail(email) == False:

            return JsonResponse({
                'result': 'ERR',
                'error': {
                    'key': 'INVALID_EMAIL_ADDRESS'
                }
            })
        else:

            # TODO token must be set after confirmation
            token = jwt.encode({'firstName': firstName, 'lastName': lastName, 'email': email}, 'SECRET', algorithm='HS256')
            ##SHA256?

            #import hashlib
            #hash_object = hashlib.sha256(b'Hello World')
            #hex_dig = hash_object.hexdigest()
            #print(hex_dig)



            user = User(firstName=firstName, lastName=lastName, password=hashlib.sha256(password.encode()).hexdigest(), email=email, token=token)
            user.save()

            return JsonResponse(
                {
                    'result': 'OK',
                    'data': {
                        'token': str(token)
                    }
                },
            )


@csrf_exempt
def login(request):
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        email = body.get('email', None)
        password = body.get('password', None)
        #TODO validation

        users = User.objects.filter(email=email, password=hashlib.sha256(password.encode()).hexdigest())
        if users is None or len(users) == 0:
            return JsonResponse({
                'result': 'ERR',
                'error': {
                    'key': 'EMAIL_OR_PASSWORD_IS_WRONG'
                }
            })
        return JsonResponse({
            'result': 'OK',
            'data': {
                'userId': str(users[0].id),
                'token': str(users[0].token)
            }
        })


def show_sentence_history(request, userId):
    # TODO only admin can see
    if request.method == 'GET':
        authorization_error, user = authorization_and_get_user(request, userId)
        if authorization_error is not None:
            return authorization_error

        sentence_histories = SentenceHistory.objects.filter(userId=userId)
        return JsonResponse({
            'result': 'OK',
            'data': {
                'sentence_histories': json.loads(sentence_histories.to_json())
            }
        })


def profile(request, userId):
    if request.method == 'GET':
        #authorization_error, user = authorization_and_get_user(request, userId)
        #if authorization_error is not None:
        #    return authorization_error
        user = User.objects.filter(id=userId)

        return JsonResponse({
            'result': 'OK',
            'data': {
                'firstName': user[0]['firstName'],
                'lastName': user[0]['lastName'],
                'email': user[0]['email'],
                'bio': user[0]['bio'],
                'score': user[0]['score']
            }
        })

@csrf_exempt
def edit_profile(request, userId):
    #authorization_error, user = authorization_and_get_user(request, userId)
    #if authorization_error is not None:
    #    return authorization_error
    user = User.objects.filter(id=userId)

    if request.method == 'POST':
        body = json.loads(request.body)
        # TODO validation
        firstName = body.get('firstName', None)
        lastName = body.get('lastName', None)
        email = body.get('email', None)
        password = body.get('password', None)
        bio = body.get('bio', None)

        user[0].firstName = firstName
        user[0].lastName = lastName
        user[0].email = email
        user[0].password = hashlib.sha256(password.encode()).hexdigest()
        user[0].bio = bio
        user[0].save()

        return JsonResponse({
            'result': 'OK',
            'data': {
                'firstName': str(user[0].firstName),
                'lastName': str(user[0].lastName),
                'email': str(user[0].email),
                'password': str(user[0].password),
                'bio': str(user[0].bio)
            }
        })