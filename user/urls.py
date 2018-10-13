from django.conf.urls import url
from user import views

app_name = "user"

urlpatterns = [
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^(?P<userId>[a-z0-9]*)/edit_profile$', views.edit_profile, name='edit_profile'),
    url(r'^(?P<userId>[a-z0-9]*)/profile$', views.profile, name='profile'),
    url(r'^(?P<userId>[a-z0-9]*)/history$', views.show_sentence_history, name='sentence'),
]
