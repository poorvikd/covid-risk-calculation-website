from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
import json
import os
from django.views.decorators.csrf import csrf_exempt
from .models import *
from math import floor
import requests
import datetime
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import textwrap
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
status={
    'red':'Danger',
    'orange':'High Risk',
    'yellow':'Risk',
    'blue':'Moderate Risk',
    'green':'Safe'
}
inter = {
    'red': 'Emergency!! You have declared serious COVID-19 Symptoms during the self-assessment. Please get admitted to a Health care facility immediately. Get tested for COVID-19 as soon as possible. Alert people who have been in close contact to you. Monitor your Symptoms and update it to your Doctor. (Call 108/104 if the suspect is exhibiting severe symptoms)',
    'orange': 'Don’t Panic! You have declared COVID-19 Symptoms during the self-assessment. Please Self-Isolate yourself/ get admitted to a Health care facility. Get tested for COVID-19 as soon as possible. Alert people who have been in close contact to you. Monitor your Symptoms and update it to your Doctor. (Call 108/104 if the suspect is exhibiting severe symptoms)',
    'yellow': 'Oh! You have indicated one/more COVID-19 Symptoms during the self-assessment. It’s better to Self-Isolate yourself at home and keep monitoring your symptoms. Take medical advice if feeling uncomfortable.',
    'blue': 'Good! You need not worry. You may have indicated a Mild COVID-19 Symptom during the self-assessment. Keep monitoring your symptoms & take a Medical advice if it continues. Stay safe and take precautions.',
    'green': 'Great! You haven’t declared one or more suspected COVID-19 Symptoms during the self-assessment. Spread awareness and let us end the pandemic! Stay safe and continue with precautions.'
}
remark = {
    'red': 'Immediately contact a Health Care Facility and get tested for COVID-19.',
    'orange': 'Stay in Home Isolation till you get tested and recieve the result for COVID-19. Contact Health Care giver if facing longer symptoms.',
    'yellow': 'Stay in Home Quarantine and monitor your symptoms for 1-2 weeks.',
    'blue': 'Advised not to leave your home unless mandatory for precautionary 1-2 weeks. Regularly monitor symptoms.',
    'green': 'You are free to resume your duties. Take all necessary precations.'
}
table = {
    'com': ["It may not always be COVID-19. These common symptoms can be due to other factors too.", "You haven't announced any of the common symptoms."],
    'mod': ["You have selected one or more suspected COVID-19 Symptoms.", "You haven't announced any of the moderate symptoms."],
    'sev': ["You have selected one or more severe COVID-19 Symptoms. May cause serious threat, get medical help soon.", "You haven't announced any of the severe symptoms."],
    'co' : ["Those with underlying medical conditions are at higher risk and require more care."],
    'tr': ["Traveling may help virus spread. Travel only if necessary."],
    'exp': ["Check for any symptoms. If suspected get tested. Wear Mask. Save Lives.", "You haven't revealed any such case. Wear Mask. Save Lives."]
}
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
        res = requests.get(f'https://api.covid19api.com/country/{self.country}/status/confirmed?from={self.two_weeks_before}&to={self.today}')
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
    user = User.objects.all().last()
    med = MedicalInfo.objects.filter(name=user).last()
    travel = TravelInfo.objects.filter(name=user).last()
    score = Score()
    score.name = user
    score.total_score=s=calculate_score(med.medical_score,travel.travel_score)
    score.save()
    color = determine_color(s)
    img_name=generate_graph(s,color,user.id)
    context={}
    context['img']=img_name
    context['user']=user
    context['score']=s
    context['interpretation']=inter[color[0]]
    context['remark']=remark[color[0]]
    context['color']=color[0]
    if request.method  == "POST":
        generate_report(user,med,travel,color[0],s)
        email_to_user(user)
        return HttpResponseRedirect(reverse("home"))
    return render(request,"chatbot/score.html",context)
def generate_report(user,med,travel,color,score):
    im = Image.open(f"{STATIC_ROOT}/images/report.jpg")
    d = ImageDraw.Draw(im)
    location_name = (400, 315)
    text_color = (0, 0, 0)
    font = ImageFont.truetype(f"{STATIC_ROOT}/fonts/tnr.ttf", 50)
    d.text(location_name,user.name, fill=text_color, font=font)
    location_email = (1560, 315)
    d.text(location_email, user.email, fill=text_color, font=font)
    location_date = (760, 400)
    d.text(location_date, str(user.date),fill=text_color, font=font)
    location_age = (1500, 400)
    d.text(location_age, str(user.age),fill=text_color, font=font)
    location_temp = (1180, 735)
    d.text(location_temp, str(med.temperature),fill=text_color, font=font)
    com, com_count = get_common_symptoms_text(med)
    if com_count > 0:
        com_remark = table['com'][0]
    else:
        com="None"
        com_remark = table['com'][1]
    font_1 = ImageFont.truetype(f"{STATIC_ROOT}/fonts/tnr.ttf", 40)
    location_com_1 = (585, 930)
    com=wrap(com,55)
    com_remark = wrap(com_remark,30)
    d.text(location_com_1, com,fill=text_color, font=font_1)
    location_com_2=(1530,910)
    d.text(location_com_2,com_remark,fill=text_color, font=font_1)
    location_mod_1=(590,1050)
    mod, mod_count = get_moderate_symptoms_text(med)
    if mod_count > 0:
        mod_remark = table['mod'][0]
    else:
        mod = "None"
        mod_remark = table['mod'][1]
    mod=wrap(mod,55)
    mod_remark = wrap(mod_remark,30)
    d.text(location_mod_1, mod,fill=text_color, font=font_1)
    location_mod_2 = (1530, 1070)
    d.text(location_mod_2, mod_remark,fill=text_color, font=font_1)
    sev, sev_count = get_severe_symptoms_text(med)
    if sev_count > 0:
        sev_remark = table['sev'][0]
    else:
        sev = "None"
        sev_remark = table['sev'][1]
    sev = wrap(sev, 55)
    sev_remark = wrap(sev_remark, 30)
    location_sev_1 = (590, 1260)
    d.text(location_sev_1, sev, fill=text_color, font=font_1)
    location_sev_2 = (1530, 1245)
    d.text(location_sev_2, sev_remark,fill=text_color, font=font_1)
    co, co_count = get_comorbidity_text(med)
    if co_count > 0:
        co_remark = table['co'][0]
    else:
        co = "None"
        co_remark = table['co'][0]
    co = wrap(co, 50)
    co_remark = wrap(co_remark, 30)
    location_co_1 = (590, 1430)
    d.text(location_co_1,co, fill=text_color, font=font_1)
    location_co_2 = (1530, 1445)
    d.text(location_co_2, co_remark,fill=text_color, font=font_1)
    tr, tr_count = get_travel_text(travel)
    if tr_count > 0:
        tr_remark = table['tr'][0]
    else:
        tr = "None"
        tr_remark = table['tr'][0]
    tr = wrap(tr, 50)
    tr_remark = wrap(tr_remark, 35)
    location_tr_1 = (590, 1640)
    d.text(location_tr_1, tr,fill=text_color, font=font_1)
    location_tr_2 = (1530, 1620)
    d.text(location_tr_2, tr_remark,fill=text_color, font=font_1)
    exp, exp_count = get_exposure_text(med)
    if exp_count > 0:
        exp_remark = table['exp'][0]
    else:
        exp = "None"
        exp_remark = table['exp'][1]
    exp = wrap(exp, 50)
    exp_remark = wrap(exp_remark, 30)  
    location_ex_1 = (590, 1760)
    d.text(location_ex_1, exp, fill=text_color, font=font_1)
    location_ex_2 = (1530, 1760)
    d.text(location_ex_2, exp_remark, fill=text_color, font=font_1)
    text_color_1 = rgb(color)
    location_i = (170, 2100)
    interpretation = wrap(inter[color],50)
    d.text(location_i, interpretation,fill=text_color_1, font=font_1)
    font_2 = ImageFont.truetype(f"{STATIC_ROOT}/fonts/tnr.ttf", 50)
    location_rp = (1690, 2000)
    d.text(location_rp, f"{str(score)}%", fill=text_color_1, font=font_2)
    location_rs = (1570, 2070)
    d.text(location_rs, status[color] , fill=text_color_1, font=font_2)
    location_remarks = (310, 2730)
    rem = wrap(remark[color],90)
    d.text(location_remarks,rem,fill=text_color_1, font=font_2)
    location_img_tl = (1170,2200)
    location_img_tr = (1600,2200)
    location_img_bl = (1170,2600)
    location_img_br = (1600,2600)
    im1 = Image.open(f'{STATIC_ROOT}/graphs/graph_{user.id}.png')
    im1=im1.resize((400, 400), resample=0)
    im.paste(im1, location_img_tl)
    im.save(f'{STATIC_ROOT}/reports/report-{user.id}.pdf')
    return
def rgb(color):
    if color == "red":
        return (255,0,0)
    if color == "orange":
        return (255,102,0)
    if color == "yellow":
        return (226, 172, 0)
    if color == "blue":
        return (0, 112, 192)
    if color == "green":
        return (0, 128, 0)

def email_to_user(user):
    fromaddr = "crc19.pbl@gmail.com"
    toaddr = str(user.email)
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Your Covid-19 risk analysis by CRC-19"
    intro = "Greetings!\n"
    msg.attach(MIMEText(intro, 'plain'))
    body = "We hope that you are doing well. Please find attached copy of your Covid-19 risk analysis report.\n"
    msg.attach(MIMEText(body, 'plain'))
    filename = f'/Users/Kiran/Desktop/Project/rasa/covid-risk-calculation-website/crc19/chatbot/static/reports/report-{user.id}.pdf'
    attachment = open(filename, "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', f"attachment; filename= report-{ user.name }.pdf"  )
    msg.attach(p)
    conclusion = "Regards\n"
    msg.attach(MIMEText(conclusion, 'plain'))
    t = "Team CRC-19\n"
    msg.attach(MIMEText(t, 'plain'))
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, "Django@pbl")
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()
    return
def wrap(text,width):
    wrapper = textwrap.TextWrapper(width=width)
    word_list = wrapper.wrap(text=text)
    text_new = ''
    for ii in word_list[:-1]:
       text_new = text_new + ii + '\n'
    text_new += word_list[-1]
    return text_new
def get_exposure_text(medical):
    exp_str=""
    count=0
    if medical.lived_covid == True:
        count+=1
        exp_str+="Recently interacted or lived with someone who has been tested COVID-19 Positive, "
    if medical.frontline == True:
        count += 1
        exp_str += "I'm a Frontline/Healthcare worker who have examined a COVID-19 confirmed case without proctective gear, "
    if medical.crowded == True:
        count+=1
        exp_str += "Been to a crowded place without protection/Travelled in Public transport without protection, "
    if medical.gathering == True:
        count+=1
        exp_str += "Attended a gathering/event, "
    if medical.containment == True:
        count+=1
        exp_str += "Living in COVID containment area, "
    return (exp_str,count)
def get_travel_text(travel):
    count=0
    tr_text=""
    if travel.intl==True:
        count+=1
        tr_text+=f"{travel.i_destination}, "
    if travel.natl==True:
        count+=1
        tr_text+=f"{travel.n_destination}, "
    return (tr_text,count)
def get_common_symptoms_text(medical):
    com_str=""
    count=0
    if medical.fever == True:
        count+=1
        com_str+="Fever, "
    if medical.cold == True:
        count += 1
        com_str += "Cold & Excessive Sneezing, "
    if medical.dry_cough == True:
        count+=1
        com_str+="Dry Cough, "
    if medical.nasal == True:
        count+=1
        com_str+="Nasal Congestion, "
    if medical.tired == True:
        count+=1
        com_str+="Tiredness, "
    if medical.headache==True:
        count+=1
        com_str += "Headache,"
    return (com_str,count)
def get_comorbidity_text(medical):
    co_str=""
    count=0
    if medical.lung == True:
        count+=1
        co_str += "Lung Disease(Asthma,COPD,TB,etc), "
    if medical.heart == True:
        count += 1
        co_str += "Heart Disease, "
    if medical.cancer == True:
        count+=1
        co_str+="Cancer, "
    if medical.hypten == True:
        count+=1
        co_str+="Hypertension, "
    if medical.diabetes == True:
        count+=1
        co_str+="Diabetes, "
    if medical.kidney==True:
        count+=1
        co_str += "Kidney Disorder, "
    if medical.stroke==True:
        count+=1
        co_str += "Stroke, "
    if medical.immunity==True:
        count+=1
        co_str += "Reduced Immunity, "
    if medical.liver==True:
        count+=1
        co_str+="Chronic Liver Disease, "
    return (co_str,count)
def get_severe_symptoms_text(medical):
    sev_str=""
    count=0
    if medical.breathe == True:
        count+=1
        sev_str+="Difficulty in breathing or shortness of breath, "
    if medical.chest_pain == True:
        count += 1
        sev_str += "Chest pain or pressure, "
    if medical.speech_loss == True:
        count+=1
        sev_str += "Loss of speech or movement, "
    if medical.uncon == True:
        count+=1
        sev_str += "Unconsciousness, "
    return (sev_str,count)
def get_moderate_symptoms_text(medical):
    mod_str = ""
    count = 0
    if medical.smell == True:
        count += 1
        mod_str += "Loss of Smell & Taste, "
    if medical.body_ache == True:
        count += 1
        mod_str += "Body Aches and Pains, "
    if medical.nausea == True:
        count += 1
        mod_str += "Nausea,Vomiting,and Diarrhoea, "
    if medical.sore_throat == True:
        count += 1
        mod_str += "Sore Throat, "
    if medical.conjunctivitis == True:
        count += 1
        mod_str += "Conjunctivitis, "
    if medical.rash == True:
        count += 1
        mod_str += "Rash on Skin, "
    if medical.discolor == True:
        count += 1
        mod_str += "Discoloration, "
    return (mod_str, count)
    
    
def determine_color(score):
    if score>0 and score<20:
        return ["green","white"]
    elif score>=20 and score<40:
        return ["blue","white"]
    elif score>=40 and score<60:
        return ["yellow","white"]
    elif score>=60 and score<80:
        return ["orange","white"]
    elif score>=80 and score<100:
        return ["red","white"]
def calculate_score(med,travel):
    s = med+travel
    sp = round(((s*100)/168),2)
    return sp
def generate_graph(score,color,id):
    size=[score,100-score]
    my_circle=plt.Circle( (0,0), 0.7, color='white')
    a,b,c = rgb(color[0])
    color=(a/255,b/255,c/255)
    plt.pie(size, colors=[color,(1,1,1)], startangle=90, wedgeprops={"edgecolor": "0", 'linewidth': 1,'linestyle': 'solid', 'antialiased': True})
    p = plt.gcf()
    p.gca().add_artist(my_circle)
    plt.savefig(f'{STATIC_ROOT}/graphs/graph_{id}.png')
    return f'graphs/graph_{id}.png'
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
    


