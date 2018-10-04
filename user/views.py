import json, jwt

from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from tagger.models import SentenceHistory
from user.models import User


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
        body = json.loads(request.body.decode('utf-8'))
        #TODO validation
        firstName = body.get('firstName', None)
        lastName = body.get('lastName', None)
        email = body.get('email', None)
        password = body.get('password', None)
        confirmPassword = body.get('confirmPassword', None)
        if password != confirmPassword:
            return JsonResponse(
                {
                    'result': 'ERR',
                    'error': {
                        'key': 'PASSWORD_AND_CONFIRM_DOES_NOT_MATCH'
                    }
                }
            )

        #TODO token must be set after confirmation
        token = jwt.encode({'firstName': firstName, 'lastName': lastName, 'email': email}, 'SECRET', algorithm='HS256')

        user = User(firstName=firstName, lastName=lastName, password=password, email=email, token=token)
        user.save()

        return JsonResponse(
            {
                'result': 'OK',
                'data': {
                    'userId': str(user.id),
                    'token': str(token, encoding='utf-8')
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
        users = User.objects.filter(email=email, password=password)
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
        authorization_error, user = authorization_and_get_user(request, userId)
        if authorization_error is not None:
            return authorization_error

        return JsonResponse({
            'result': 'OK',
            'data': {
                'firstName': user['firstName'],
                'lastName': user['lastName'],
                'email': user['email'],
                'bio': user['bio'],
                'score': user['score']
            }
        })