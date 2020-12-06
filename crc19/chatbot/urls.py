from django.urls import path
from .views import *
urlpatterns=[path('',index,name="home"),
             path('about',about,name="about"),
             path('news',news,name='news'),
             path('assessment',assessment,name="assessment"),
             path('team',team,name="team"),
             path('action',action,name="action"),
             path('medform/<int:user_id>',medform,name="medform"),
             path('travelform/<int:user_id>',travelform,name="travelform"),
             path("score/<int:user_id>",score,name="score"),
             ]
