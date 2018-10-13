from django.conf.urls import url

from ticketing import views

app_name = "ticketing"

urlpatterns = [

    url(r'^(?P<userId>[a-z0-9]*)/tickets', views.tickets, name='tickets')
]
