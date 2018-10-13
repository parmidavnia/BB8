import json

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

#from ticketing.models import Ticket
from ticketing.models import Ticket
from user.models import User
from user.views import authorization_and_get_user


@csrf_exempt
def tickets(request, userId):


    #user = User.objects.filter(id=userId)
    if request.method == 'POST':
        user = User.objects.filter(id=userId)
        body = json.loads(request.body)

        text = body.get('text', None)

        ticket=Ticket(text=text, userId=user[0].id)
        ticket.save()
        return HttpResponse("successful")
    elif request.method == 'GET':
        # authorization_error, user = authorization_and_get_user(request, userId)
        # if authorization_error is not None:
        #    return authorization_error

        tickets=Ticket.objects.all()
        response = []
        for ticket in tickets:

            user = User.objects.filter(id=userId)
            response.append({"text":ticket.text, "email":user[0].email})


        return JsonResponse({'tickets': response})
