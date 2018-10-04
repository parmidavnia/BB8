from django.conf.urls import url
from tagger import views

app_name = "tagger"

urlpatterns = [
    url(r'^$', views.add_sentence, name='addSentence'),
    url(r'^(?P<page>[a-z0-9]*)/(?P<limit>[a-z0-9]*)$', views.get_all_sentences, name='get_all_sentences'),
    url(r'^(?P<sentenceId>[a-z0-9]*)$', views.sentence, name='sentence'),
]
