from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()
    def __str__(self):
        return f"{self.name}"
class MedicalInfo(models.Model):
    temperature = models.DecimalField( max_digits=5,decimal_places=2)
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="medical_info")
    fever = models.BooleanField(default=False)
    dry_cough = models.BooleanField(default=False)
    nasal = models.BooleanField(default=False)
    tired = models.BooleanField(default=False)
    headache = models.BooleanField(default=False)
    cold = models.BooleanField(default=False)
    smell = models.BooleanField(default=False)
    body_ache = models.BooleanField(default=False)
    sore_throat = models.BooleanField(default=False)
    nausea = models.BooleanField(default=False)
    conjunctivitis = models.BooleanField(default=False)
    rash = models.BooleanField(default=False)
    discolor = models.BooleanField(default=False)
    breathe = models.BooleanField(default=False)
    chest_pain = models.BooleanField(default=False)
    speech_loss = models.BooleanField(default=False)
    uncon = models.BooleanField(default=False)
    lung = models.BooleanField(default=False)
    heart = models.BooleanField(default=False)
    cancer = models.BooleanField(default=False)
    hypten = models.BooleanField(default=False)
    diabetes = models.BooleanField(default=False)
    kidney = models.BooleanField(default=False)
    liver = models.BooleanField(default=False)
    stroke = models.BooleanField(default=False)
    immunity = models.BooleanField(default=False)
    lived_covid = models.BooleanField(default=False)
    frontline = models.BooleanField(default=False)
    crowded = models.BooleanField(default=False)
    gathering = models.BooleanField(default=False)
    containment = models.BooleanField(default=False)
    medical_score = models.DecimalField(max_digits=7,decimal_places=3)
    def __str__(self):
        return f"{self.name}-Medical"
class TravelInfo(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="travel_info")
    intl = models.BooleanField(default=False)
    natl = models.BooleanField(default=False)
    i_destination = models.CharField(max_length = 100,blank=True, null=True)
    n_destination = models.CharField(max_length=100,blank=True, null=True)
    travel_score = models.DecimalField(max_digits=7,decimal_places=3)
    def __str__(self):
        return f"{self.name}-Travel"
class Score(models.Model):
    name = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_score")
    total_score = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return f"{self.name}-Score"
