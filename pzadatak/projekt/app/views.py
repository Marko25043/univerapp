from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import SubjectForm,ProfessorForm,StudentForm,EnrollmentForm,AddSubject
from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from .decorators import professor_required,admin_required,student_required
from django.http import JsonResponse
from .models import Korisnik,Uloga,Predmet,Upisi

def home(request):
    users = Korisnik.objects.all()
    return render(request, 'login.html', {"data":users})

def hello(request):
    return render(request, 'main.html', {"data":request.user})

def login_user(request):
    text ='login'
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
         return render(request, 'login.html',{'text':text})

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
@admin_required
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

#popis upisanih studenata po kolegiju      
@login_required(login_url='login')
@admin_required
def enrolled_students(request,pk):
    enrollment = Upisi.objects.filter(subject_id = pk)
    students =[{'username':enroll.student.username,'status':enroll.status,
                'id':enroll.pk,
                'subject_name':enroll.subject.name
                } for enroll in enrollment]
    return render(request, 'enrolled_students.html', {'students': students})

@login_required(login_url='login')
@admin_required
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
def add_enrollment_form(request):
    if request.method == 'GET':
        form = EnrollmentForm()
        enrollments = Upisi.objects.all().order_by('student__username')
        return render(request, 'add_enrollment_form.html', {"form":form,'enrollments':enrollments})
    elif request.method == 'POST':
        form = EnrollmentForm(request.POST)
        print(request.POST)
        if form.is_valid():
                form.save()
                return redirect('main')
        else:
            return render(request, 'add_enrollment_form.html', {"form":form,'enrollments':enrollments})

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

def delete_atrribute(request,pk,ModelName,url_name,html_name):
    object_name = ModelName.objects.get(id = pk)
    if request.method == 'POST':
        object_name.delete()
        return redirect(url_name)
    return render(request,html_name,{'obj':object_name})


@login_required(login_url='login')
@admin_required
def update_professor(request, pk):
    return update_record(request, pk, Korisnik, ProfessorForm, 'add_professor', 'add_professor.html')

@admin_required
@login_required(login_url='login')
def update_student(request, pk):
     return update_record(request, pk, Korisnik, StudentForm, 'add_student', 'add_student.html')

@login_required(login_url='login')
def update_subject(request, pk):
     return update_record(request, pk, Predmet, SubjectForm, 'add_subject', 'add_subject.html')

@login_required(login_url='login')
def update_enrollment_form(request, pk):
     return update_record(request, pk, Upisi, EnrollmentForm, 'add_enrollment_form', 'add_enrollment_form.html')

#Update status - Professor panel
@login_required(login_url='login')
@professor_required
def update_student_status(request, pk):
    return update_record(request, pk, Upisi, EnrollmentForm, 'professor', 'update_student_status.html')

#Update status - Admin panel
@admin_required
def admin_update_student_status(request, pk):
    return update_record(request, pk, Upisi, EnrollmentForm, 'add_subject', 'update_student_status.html')


@login_required(login_url='login')
@admin_required
def delete_professor(request, pk):
    return delete_atrribute(request,pk,Korisnik,"add_professor","delete.html")

@login_required(login_url='login')
def delete_student(request, pk):
    return delete_atrribute(request,pk,Korisnik,"add_student","delete.html")

@login_required(login_url='login')
def delete_subject(request, pk):
    return delete_atrribute(request,pk,Predmet,"add_subject","delete.html")

@login_required(login_url='login')
def delete_enrollment_form(request, pk):
    return delete_atrribute(request,pk,Upisi,"add_enrollment_form","delete.html") 

#Professor Panel
@login_required(login_url='login')
@professor_required
def professor(request):
    user = request.user
    subjects =Predmet.objects.filter(user_id = user.id)
    print(subjects) 
    return render(request, 'professor.html', {'data':user,'subjects':subjects})

#svi studenti odredenog profesora upisanih na kolegij
@login_required(login_url='login')
@professor_required
def professor_enrolled_student(request,pk):
    enrollment = Upisi.objects.filter(subject_id = pk)
    print('testiranje ',enrollment)
    students =[{'username':enroll.student.username,
                'status':enroll.status,
                'id':enroll.pk,
                'subject_name':enroll.subject.name
                } 
                for enroll in enrollment]
    print(students)
    return render(request, 'enrolled_students.html', {'students': students})


#studentska statistika po predmetu
@login_required(login_url='login')
@professor_required
def student_statistics_by_subject(request,pk):
    enrollment = Upisi.objects.filter(subject_id = pk)
    number_of_enrolled = enrollment.count()
    enrollment =[{'username':enroll.student.username,
                'status':enroll.status,
                'id':enroll.pk,
                'subject_name':enroll.subject.name
                } 
                for enroll in enrollment]
    number_of_passed = sum(1 for enroll in enrollment if enroll['status'] == 'P')
    number_of_failed = sum(1 for enroll in enrollment if enroll['status'] == 'N')
    # return JsonResponse({'enrollment':list(enrollment)})
    return render(request,'professor.html', {'enrollment':enrollment,'enrolled':number_of_enrolled,
                                            'failed':number_of_failed, 'passed':number_of_passed})

def filter_enrollment_by_student_id(request, pk):
     enrollment = Upisi.objects.filter(student_id = pk)
     enrollment =[{
                'status':enroll.status,
                'name':enroll.subject.name,
                'code':enroll.subject.code,
                'ects':enroll.subject.ects,
                } 
                for enroll in enrollment]
     return enrollment

#Student Panel
@login_required(login_url='login')
@student_required
def student(request):
    view_message='view_student' 
    enrollment = filter_enrollment_by_student_id(request, request.user.id)
    return render(request, 'student.html', {"data":request.user,"view_message":view_message,"enrollment":enrollment})

def student_add_subject(request):

    if request.method == 'GET':
        form = AddSubject(student = request.user)
        return render(request, 'student.html', {"form":form})
    
    elif request.method == 'POST':
        form = AddSubject(request.POST)
        if form.is_valid():
                form.save()
                return redirect('student')
        else:
          return render(request, 'student.html', {"form":form})