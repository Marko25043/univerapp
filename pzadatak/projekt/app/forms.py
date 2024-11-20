from django.forms import ModelForm
from .models import Predmet,Korisnik,Upisi
from django.contrib.auth.hashers import make_password
from django import forms

class SubjectForm(ModelForm):
        class Meta :
                model = Predmet
                fields = '__all__'

        def __init__(self, *args, **kwargs):
            super(SubjectForm, self).__init__(*args, **kwargs)
            #postavljanje svih korisnika koji imaju role_id 8 to jest da su profesori
            self.fields['user'].queryset = Korisnik.objects.filter(role_id=8)           
    
class ProfessorForm(ModelForm):
       class Meta :
                model = Korisnik
                fields = ['username','password','email','status','role']
                widgets={
                       'password': forms.PasswordInput(),
                       'role':forms.HiddenInput(),
                    #    'status':forms.HiddenInput()
                }
                
       def clean_password(self):
              password = make_password(self.cleaned_data.get('password'))
              return password
    
       def __init__(self,*args, **kwargs):
              super(ProfessorForm, self).__init__(*args, **kwargs)
              self.fields['role'].initial = 8
            #   self.fields['status'].initial = "None"

class StudentForm(ModelForm):
       class Meta :
                model = Korisnik
                fields = ['username','password','email','status','role']
                widgets={
                       'password': forms.PasswordInput(),
                       'role':forms.HiddenInput(),
                }
                
       def clean_password(self):
              password = make_password(self.cleaned_data.get('password'))
              return password
    
       def __init__(self,*args, **kwargs):
              super(StudentForm, self).__init__(*args, **kwargs)
              self.fields['role'].initial = 7
      
class EnrollmentForm(ModelForm):
        class Meta :
                model = Upisi
                fields = '__all__'

        def __init__(self, *args, **kwargs):
              super(EnrollmentForm, self).__init__(*args, **kwargs)
              self.fields['student'].queryset = Korisnik.objects.filter(role_id=7)           
           

class AddSubject(ModelForm):
       status =forms.CharField(widget=forms.HiddenInput(),initial='U')
       class Meta:
              model = Upisi
              fields =['subject','student']
              widgets={
                       'student':forms.HiddenInput(),
                }

       def __init__(self,*args, **kwargs):
              student = kwargs.pop('student', None) #dohvati student iz kwargsa
              super(AddSubject, self).__init__(*args, **kwargs)

              enrolled_subjects = Upisi.objects.filter(student=student).values_list('subject', flat=True)
              print("Upisani predmeti testiranje",enrolled_subjects)
              self.fields['subject'].queryset = Predmet.objects.exclude(id__in=enrolled_subjects)

              self.fields['student'].initial = student
            #   self.fields['status'].initial = "None"

    