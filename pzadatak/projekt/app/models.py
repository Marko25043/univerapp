from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Uloga(models.Model):
    ROLES =(('Professor','profesor'),('Student','student'),('Admin','admin'))
    role = models.CharField(max_length = 50, choices = ROLES,default="admin")

    def __str__(self):
        return self.role

class Korisnik(AbstractUser):
    STATUS = (('none', 'None'), ('izv', 'izvanredni student'), ('red', 'redovni student'))
    status = models.CharField(max_length = 50, choices = STATUS)
    role = models.ForeignKey(Uloga,on_delete=models.CASCADE,blank=True, null=True)
    
    email = models.EmailField(unique=True)

    
    def __str__(self):
        return '%s %s %s' % (self.username,self.email,self.role)

class Predmet(models.Model):
    IZBORNI = (('DA', 'da'), ('NE', 'ne'))
    name =  models.CharField(max_length = 60)
    code = models.CharField(max_length = 30)
    program = models.CharField(max_length=50)
    ects = models.IntegerField()
    user = models.ForeignKey(Korisnik,on_delete=models.CASCADE,blank=True, null=True)
    sem_red = models.IntegerField(default=1)
    sem_izv = models.IntegerField(default=1)
    izborni = models.CharField(max_length=50, choices=IZBORNI,default='NE')

    def __str__(self):
        return '%s %s %s %s' % (self.name, self.code,self.ects, self.user)


class Upisi(models.Model):
    STATUS =(('P','Polozeno'),('N','Nepolozeno'),('U','Upisano'),('PU','PONOVNO UPISANO'))
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Korisnik,on_delete=models.CASCADE,blank=True, null=True)
    subject = models.ForeignKey(Predmet,on_delete=models.CASCADE,blank=True, null=True)
    status = models.CharField(max_length = 65,choices=STATUS,default='U')

    class Meta:
        unique_together = ('student', 'subject')
 

    def __str__(self):
        return '%s %s %s %s' % (self.status, self.student_id, self.subject_id,self.get_status_display())