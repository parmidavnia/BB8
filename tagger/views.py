import csv
import json

from django.http.response import Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from tagger.models import Sentence, SentenceHistory
from user.models import User


def admin_authorization(request):
    auth_token = request.META.get('HTTP_AUTH', None)
    users = User.objects.filter(token=auth_token)
    if users is None or len(users) == 0:
        return JsonResponse({
            'result': 'ERR',
            'error': {
                'key': 'AUTHENTICATION_ERROR'
            }
        })

    user = users[0]

    if user['role'] != 'ADMIN':
        return JsonResponse({
            'result': 'ERR',
            'error': {
                'key': 'AUTHORIZATION_ERROR'
            }
        })
    return None


@csrf_exempt
def add_sentence_from_file(request):
    if request.method == 'GET':
        #authorization_error = admin_authorization(request)
        #if authorization_error is not None:
        #    return authorization_error


        with open('InputFile.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter="\n")

            for text in csv_reader:

                print(text[0])

                s = Sentence(text=text[0])
                s.save()

            return JsonResponse({
                'result': 'OK',
                'data': {
                    'sentence': json.loads(s.to_json())
                }
            }, safe=False)




def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@csrf_exempt
def add_sentence(request):
    if request.method == 'POST':
        #authorization_error = admin_authorization(request)
        #if authorization_error is not None:
        #    return authorization_error

        body = json.loads(request.body.decode('utf-8'))
        text = body.get('text', None)

        if text is None or text.strip() == '':
            return JsonResponse({
                'result': 'ERR',
                'error': {
                    'key': 'TEXT_IS_EMPTY_ERROR'
                }
            })
        s = Sentence(text=text)
        s.save()
        return JsonResponse({
            'result': 'OK',
            'data': {
                'sentence': json.loads(s.to_json())
            }
        }, safe=False)


@csrf_exempt
def sentence(request, sentenceId):
    sentences = Sentence.objects.filter(id=sentenceId)
    if sentences is None or len(sentences) == 0:
        raise Http404
    sentence = sentences[0]
    if request.method == 'GET':
        return JsonResponse({
            'result': 'OK',
            'data': {
                'sentence': json.loads(sentence.to_json())
            }
        }, safe=False)

    elif request.method == 'PUT':
        # TODO refactor
        body = json.loads(request.body.decode('utf-8'))
        polarity = body.get('polarity', None)
        if polarity is None:
            return JsonResponse({
                'result': 'ERR',
                'error': {
                    'key': 'SCORE_IS_NONE'
                }
            })
        sentence_dict = json.loads(sentence.to_json())

        avg = ((polarity * 0.2) + (sentence_dict['polarityAvg'] * 0.8))
        sentence.update(polarityAvg=avg)

        auth_token = request.META.get('HTTP_AUTH', None)
        # TODO refactor => security issue
        userId = None
        if auth_token:
            users = User.objects.filter(token=auth_token)
            if users is not None and len(users) != 0:
                user = users[0]
                userId = user.id
                user.score += 1
                user.save()
        ip = get_client_ip(request)
        sentence_history = SentenceHistory(userId=userId, sentenceId=sentenceId, polarity=polarity, ip=ip)
        sentence_history.save()
        return JsonResponse({
            'result': 'OK',
            'data': {
                'sentence': json.loads(sentence.to_json()) # TODO must show updated sentence
            }
        }, safe=False)


def get_all_sentences(request, page, limit):
    if request.method == 'GET':
     #   authorization_error = admin_authorization(request)
      #  if authorization_error is not None:
       #     return authorization_error

        page = int(page)
        limit = int(limit)

        offset = (page - 1) * limit

        sentences = Sentence.objects.skip(offset).limit(limit)
        return JsonResponse({
            'result': 'OK',
            'data': {
                'sentences': json.loads(sentences.to_json())
            }
        })