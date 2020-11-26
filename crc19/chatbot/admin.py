from django.contrib import admin

# Register your models here.
from .models import *


class MedicalInfoInline(admin.StackedInline):
    model = MedicalInfo
class TravelInfoInline(admin.StackedInline):
    model = TravelInfo


class ScoreInline(admin.StackedInline):
    model = Score

class UserAdmin(admin.ModelAdmin):
    inlines = [
        MedicalInfoInline,
        TravelInfoInline,
        ScoreInline
    ]
admin.site.register(User,UserAdmin)
admin.site.register(MedicalInfo)
admin.site.register(TravelInfo)
admin.site.register(Score)
