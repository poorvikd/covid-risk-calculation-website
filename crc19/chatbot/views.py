from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.views.decorators.csrf import csrf_exempt
from .models import *
from math import floor
import requests
import datetime
# class for travel history


class Country:
    def __init__(self, country):
        self.country = country
        today = datetime.datetime.now()
        d = datetime.timedelta(days=14)
        two_weeks_before = today-d
        self.today = today.date()
        self.two_weeks_before = two_weeks_before.date()
        self.edit_country(self.country)

    def edit_country(self, country):
        if len(country.split()) != 1:
            country.replace(" ", "-")
        return country

    def covid_status(self):
        res = requests.get(
            f'https://api.covid19api.com/country/{self.country}/status/confirmed?from={self.two_weeks_before}&to={self.today}')
        return res.json()

    def covid_data(self):
        vals = []
        data = self.covid_no_province()
        for i in range(len(data)-1):
            vals.append(abs(data[i+1]["Cases"]-data[i]["Cases"]))
        return int(sum(vals)/13)

    def covid_no_province(self):
        json_data = self.covid_status()
        data = []
        for i in range(len(json_data)-1):
            if (json_data[i]["Province"] == ''):
                data.append(json_data[i])
        return data

    def covid_factor(self, val):
        res = self.covid_data()
        return float((res/val)*5)
# Create your views here.
def index(request):
    return render(request,'chatbot/index.html')
def about(request):
    return render(request,'chatbot/about.html')

def news(request):
    return render(request,'chatbot/news.html')
def team(request):
    return render(request, 'chatbot/team.html')
def assessment(request):
    if request.method == "POST":
        user_details = request.POST
        user = User()
        user.name = user_details['name']
        user.age = user_details['age']
        user.email = user_details['email']
        user.save()
        return HttpResponseRedirect(reverse("medform"))
    return render(request, 'chatbot/assessment.html')
def action(request):
    return render(request,"chatbot/action.html")
def medform(request):
    user = User.objects.all().last()
    
    if request.method == "POST":
        medical = MedicalInfo()
        details = request.POST
        medical.temperature = float(details.get("temperature",0))
        medical.name = user
        medical.medical_score = 0
        medical.medical_score += age_score(medical.name.age)
        medical.medical_score += temp_score(medical.temperature)
        common_response = request.POST.getlist('com_symp')
        moderate_response = request.POST.getlist('mod_symp')
        severe_response = request.POST.getlist('sev_symp')
        comorb_response = request.POST.getlist('comorb')
        exp_response = request.POST.getlist('exposure')
        if '7' not in common_response and len(common_response)>0:
            com_count=common_symptoms(medical,common_response)
            medical.medical_score += (3+3*0.2*com_count)
        if '8' not in moderate_response and len(moderate_response)>0:
            mod_count=moderate_symptoms(medical,moderate_response)
            medical.medical_score += (5.5+5.5*0.2*mod_count)
        if '5' not in severe_response and len(severe_response)>0:
            sev_count=severe_symptoms(medical,severe_response) 
            medical.medical_score += (50+50*0.2*sev_count)
        if '10' not in comorb_response and len(comorb_response)>0:
            comorb_count=comorbidity(medical, comorb_response)
            medical.medical_score += (6+6*0.2*comorb_count)
        if '6' not in exp_response and len(exp_response)>0:
            exp_count= exposure(medical, exp_response)
            medical.medical_score += (6+6*0.2*exp_count)
        medical.save() 
        return HttpResponseRedirect(reverse("travelform"))
    return render(request, 'chatbot/medform.html')
def travelform(request):
    user = User.objects.all().last()
    if request.method == 'POST':
        details = request.POST
        travel = TravelInfo()
        travel.name = user
        travel.travel_score=0
        resp = request.POST.getlist('option')
        if '1' in  resp and '2' not in resp:
            travel.intl = True
            travel.i_destination = details.get("intl_travel","")
            travel.travel_score = intl_travel_score(travel.i_destination)
            print(f"{travel.i_destination} : {travel.travel_score}")
        elif '2' in resp:
            travel.natl = True
            travel.n_destination = details.get("natl_travel", "")
            print(travel.n_destination)
        travel.save()
        return HttpResponseRedirect(reverse("score"))


    return render(request,"chatbot/travelform.html")
def common_symptoms(med,resp):
    count=0
    if '1' in resp:
        med.fever = True
    if '2' in resp:
        count+=1
        med.dry_cough = True
    if '3' in resp:
        count += 1
        med.nasal = True
    if '4' in resp:
        count += 1
        med.tired = True
    if '5' in resp:
        count +=1
        med.headache = True
    if '6' in resp:
        count+=1
        med.cold = True
    return count


def severe_symptoms(med, resp):
    count=0
    if '1' in resp:
        count+=1
        med.breathe = True
    if '2' in resp:
        count+=1
        med.chest_pain = True
    if '3' in resp:
        count += 1
        med.speech_loss = True
    if '4' in resp:
        count += 1
        med.uncon = True
    return count


def exposure(med, resp):
    count=0
    if '1' in resp:
        count+=1  
        med.medical_score += 2
        med.lived_covid = True
    if '2' in resp:
        count += 1
        med.medical_score += 1
        med.frontline = True
    if '3' in resp:
        count += 1
        med.medical_score += 1
        med.crowded = True
    if '4' in resp:
        count += 1
        med.gathering = True
    if '5' in resp:
        count += 1
        med.containment = True
    return count

def moderate_symptoms(med, resp):
    count=0
    if '1' in resp:
        count+=1
        med.smell = True
    if '2' in resp:
        count+=1
        med.body_ache = True
    if '3' in resp:
        count+=1
        med.sore_throat = True
    if '4' in resp:
        count+=1
        med.nausea = True
    if '5' in resp:
        count += 1
        med.conjunctivitis = True
    if '6' in resp:
        count += 1
        med.rash = True
    if '7' in resp:
        count += 1
        med.discolor = True
    return count


def comorbidity(med, resp):
    count=0
    if '1' in resp:
        med.medical_score+=2
        count+=1 
        med.lung = True
    if '2' in resp:
        med.medical_score+=1
        count += 1
        med.heart = True
    if '3' in resp:
        count += 1
        med.cancer = True
    if '4' in resp:
        count += 1
        med.hypten = True
    if '5' in resp:
        count += 1
        med.diabetes = True
    if '6' in resp:
        count += 1
        med.kidney = True
    if '7' in resp:
        count += 1
        med.stroke = True
    if '8' in resp:
        count += 1
        med.immunity = True
    if '9' in resp:
        count += 1
        med.liver = True
    return count
def score(request):
    calculate_score()
    return render(request,"chatbot/score.html")
def calculate_score():
    user = User.objects.all().last()
    med = MedicalInfo.objects.filter(name=user)
    travel = TravelInfo.objects.filter(name=user)

def temp_score(temp):
    if temp>=96 and temp<=98.6:
        return 0
    elif temp>98.6 and temp<=102:
        return 3
    elif temp>102 and temp<=108:
        return (4+floor(temp-102)*0.5)
def age_score(age):
    if age>=70:
        return (4+floor(age-70)*0.2)
    elif age>=60:
        return 4
    elif age>=10:
        return 0
    elif age>=1:
        return 2
    elif age==0:
        return 3
def intl_travel_score(destination):
    c = [ "India","United Kingdom","United States","Brazil","France","Spain","Russia"]
    mx=0
    for i in c:
        co = Country(i)
        res = co.covid_data()
        if res>mx:
            mx=res
    country=Country(destination)
    return float(country.covid_factor(mx))
    
