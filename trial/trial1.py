from PIL import Image, ImageDraw, ImageFont
import textwrap
def wrap(text,width):
    wrapper = textwrap.TextWrapper(width=width)
    word_list = wrapper.wrap(text=text)
    text_new = ''
    for ii in word_list[:-1]:
       text_new = text_new + ii + '\n'
    text_new += word_list[-1]
    return text_new
im = Image.open('report.jpg')
d = ImageDraw.Draw(im)
location_name = (400, 315)
text_color = (0, 0, 0)
font = ImageFont.truetype("tnr.ttf", 50)
d.text(location_name, "Poorvik D", fill = text_color, font = font)
location_email = (1560,315)
d.text(location_email, "poorvikdharmendra@gmail.com", fill = text_color, font = font)
location_date = (760, 400)
d.text(location_date, "31/11/2020",
       fill=text_color, font=font)
location_age = (1500, 400)
d.text(location_age, "90",
       fill=text_color, font=font)
location_temp = (1200, 735)
d.text(location_temp, "108",
       fill=text_color, font=font)
location_com_1 = (585, 930)
caption=wrap("Fever, Dry Cough, Nasal Congestion, Tiredness, Headache, Cold & Excessive Sneezing",55)

font_1 = ImageFont.truetype("tnr.ttf", 40)
d.text(location_com_1, caption,
       fill=text_color, font=font_1)
location_com_2=(1530,910)
rem=wrap("It may not always be COVID-19. These common symptoms can be due to other factors too.",30)
d.text(location_com_2,rem,fill=text_color, font=font_1)
location_mod_1=(590,1050)
d.text(location_mod_1, "Loss of Smell & Taste, Body Aches and Pains,\nSore Throat, Nausea,Vomiting,and Diarrhoea,\nConjunctivitis,Rash on Skin,\nDiscoloration of Fingers or Toes",
       fill=text_color, font=font_1)
location_mod_2 = (1530, 1070)
d.text(location_mod_2, "You have selected one or more\nsuspected COVID-19 Symptoms.",
       fill=text_color, font=font_1)
location_sev_1 = (590, 1260)
d.text(location_sev_1, "Difficulty in breathing or shortness of breath,\nChest pain or pressure, Loss of speech\nor movement,Unconsciousness",
       fill=text_color, font=font_1)
location_sev_2 = (1530, 1245)
d.text(location_sev_2, "You have selected one or more\nsevere COVID-19 Symptoms.\nMay cause serious threat, get\nmedical help soon.",
       fill=text_color, font=font_1)
location_co_1 = (590, 1430)
d.text(location_co_1, "Lung Disease(Asthma,COPD,TB,etc)\nHeart Disease, Cancer, Hypertension\nDiabetes, Kidney Disorder, Stroke\nReduced Immunity, Chronic Liver Disease",
       fill=text_color, font=font_1)
location_co_2 = (1530, 1445)
d.text(location_co_2, "Those with underlying medical\nconditions are at higher risk\nand require more care.",
       fill=text_color, font=font_1)
location_tr_1 = (590, 1640)
d.text(location_tr_1, "United States of America",fill=text_color, font=font_1)
location_tr_2 = (1530, 1620)
d.text(location_tr_2, "Traveling may help virus spread.\nTravel only if necessary.",
       fill=text_color, font=font_1)
location_ex_1 = (590, 1760)
d.text(location_ex_1, "Recently interacted or lived withsomeone who has been \ntested COVID-19 Positive, I'm a Frontline/Healthcare\nworker who have examined a COVID-19 confirmed\ncase without proctective gear",
       fill=text_color, font=font_1)
location_ex_2 = (1530, 1760)
d.text(location_ex_2, "Check for any symptoms.\nIf suspected get tested.\nWear Mask. Save Lives.",
       fill=text_color, font=font_1)
text_color_1 = "red"
location_i = (170, 2100)
i = wrap("Don’t Panic! You have declared COVID-19 Symptoms during the self-assessment. Please Self-Isolate yourself/ get admitted to a Health care facility. Get tested for COVID-19 as soon as possible. Alert people who have been in close contact to you. Monitor your Symptoms and update it to your Doctor. (Call 108/104 if the suspect is exhibiting severe symptoms)",50)
d.text(location_i, i,
       fill=text_color_1, font=font_1)
font_2=ImageFont.truetype("tnr.ttf", 50)
location_rp = (1690, 2000)
d.text(location_rp, "100%",
       fill=text_color_1, font=font_2)
location_rs = (1570, 2070)
d.text(location_rs, "Moderate Risk",
       fill=text_color_1, font=font_2)
location_remarks = (310, 2730)
r = wrap("Stay in Home Isolation till you get tested and recieve the result for COVID-19. Contact\nHealthcare giver if facing longer symptoms.",90)
d.text(location_remarks, r,
       fill=text_color_1, font=font_2)
location_img_tl = (1170,2200)
location_img_tr = (1600,2200)
location_img_bl = (1170,2600)
location_img_br = (1600,2600)
im1 = Image.open(
    '/Users/Kiran/Desktop/Project/rasa/covid-risk-calculation-website/crc19/chatbot/static/graphs/graph_{id}.png')
im1=im1.resize((400,400), resample=0)
im.paste(im1,location_img_tl)
#im.show()
im.show()
