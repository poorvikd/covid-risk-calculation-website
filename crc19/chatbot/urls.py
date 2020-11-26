from django.urls import path
from .views import *
urlpatterns=[path('',index,name="home"),
             path('about',about,name="about"),
             path('news',news,name='news'),
             path('assessment',assessment,name="assessment"),
             path('team',team,name="team"),
             path('action',action,name="action"),
             path('medform',medform,name="medform"),
             path('travelform',travelform,name="travelform"),
             path("score",score,name="score"),
             ]
