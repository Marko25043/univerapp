from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import SubjectForm,ProfessorForm,StudentForm
from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required

from .models import Korisnik,Uloga,Predmet,Upisi

def home(request):
    users = Korisnik.objects.all()
    return render(request, 'login.html', {"data":users})

def hello(request):
    hello ='Pozdrav korisnik'
    return render(request, 'main.html', {"data":request.user})

def student(request):
    return render(request, 'student.html', {"data":request.user})

def professor(request):
    return render(request, 'professor.html', {"data":request.user})


def login_user(request):
    if request.method == "POST":
        # email = request.POST["email"]
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password =password )
        if user is not None:
            login(request,user)
            user_role_id = Korisnik.objects.get(username = username).role_id
            user_role = Uloga.objects.get(pk=user_role_id).role
            if user_role =="Admin":
                return redirect('main')
            elif user_role == "Student":
                return redirect('student')
            else:
                return redirect('professor')
        else:
            messages.success(request,('Pogresno uneseni podaci'))
            return redirect('login')
    else:
         return render(request, 'login.html')

@login_required(login_url='login')
def add_subject(request):
    subjects = Predmet.objects.all()
    print(subjects)
    if request.method == 'GET':
        form = SubjectForm()
        return render(request, 'add_subject.html', {"form":form,'subjects': subjects})
    elif request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
                form.save()
                return redirect('main')
        else:
          return render(request, 'add_subject.html', {"form":form,'subjects': subjects})


@login_required(login_url='login')
def add_professor(request):
    if request.method == 'GET':
        form = ProfessorForm()
        professors = Korisnik.objects.filter(role_id = 8)
        return render(request, 'add_professor.html', {"form":form,"professors":professors})
    elif request.method == 'POST':
        form = ProfessorForm(request.POST)
        if form.is_valid():
                form.save()
                return redirect('main')
        else:
            professors = Korisnik.objects.filter(role_id=8)  # Ako forma nije validna, ponovno prikaži listu profesora i formu za dodavanje
            return render(request, 'professors.html', {'professors': professors, 'form': form})

@login_required(login_url='login')
def add_student(request):
    if request.method == 'GET':
        form = StudentForm()
        students = Korisnik.objects.filter(role_id = 7)
        return render(request, 'add_student.html', {"form":form,"students":students})
    elif request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
                form.save()
                return redirect('main')
        else:
            students = Korisnik.objects.filter(role_id=7)  # Ako forma nije validna, ponovno prikaži listu profesora i formu za dodavanje
            return render(request, 'add_student.html', {"form":form,"students":students})
        
@login_required(login_url='login')
def enrolled_students(request,pk):
    enrollment = Upisi.objects.filter(subject_id = pk)
    students =[{'username':enroll.student.username,'status':enroll.status} for enroll in enrollment]

    return render(request, 'enrolled_students.html', {'students': students})

@login_required(login_url='login')
def update_student(request, pk):
     student = Korisnik.objects.get(id = pk)
     form = StudentForm(instance = student)

     if request.method == 'POST':
        form = StudentForm(request.POST, instance = student) #isto kao kod dodavanja samo saljemo instancu odabranog atributa
        if form.is_valid():
             form.save()
             return redirect('add_student')

     context ={'form':form}
     return render(request,'add_student.html',context)

# @login_required(login_url='login')
# def update_professor(request, pk):
#      professor = Korisnik.objects.get(id = pk)
#      form = ProfessorForm(instance = professor)

#      if request.method == 'POST':
#         form = ProfessorForm(request.POST, instance = professor) #isto kao kod dodavanja samo saljemo instancu odabranog atributa
#         if form.is_valid():
#              form.save()
#              return redirect('add_professor')

#      context ={'form':form}
#      return render(request,'add_professor.html',context)

def update_record(request, pk, Model, ModelForm,url,html_name):
    object_name = Model.objects.get(id = pk)
    form = ModelForm(instance = object_name)

    if request.method == 'POST':
        form = ModelForm(request.POST, instance = object_name) #isto kao kod dodavanja samo saljemo instancu odabranog atributa
        if form.is_valid():
             form.save()
             return redirect(url)

    context ={'form':form}
    return render(request,html_name,context)

@login_required(login_url='login')
def update_professor(request, pk):
    return update_record(request, pk, Korisnik, ProfessorForm,'add_professor','add_professor.html')

# @login_required(login_url='login')
# def delete_professor(request, pk):
#     professor = Korisnik.objects.get(id = pk)
#     if request.method == 'POST':
#         professor.delete()
#         return redirect('add_professor')
#     return render(request,'delete.html',{'obj':professor})


def delete_atrribute(request,pk,ModelName,url_name,html_name):
    object_name = ModelName.objects.get(id = pk)
    if request.method == 'POST':
        object_name.delete()
        return redirect(url_name)
    return render(request,html_name,{'obj':object_name})

@login_required(login_url='login')
def delete_professor(request, pk):
    return delete_atrribute(request,pk,Korisnik,"add_professor","delete.html")

@login_required(login_url='login')
def delete_student(request, pk):
    return delete_atrribute(request,pk,Korisnik,"add_student","delete.html")