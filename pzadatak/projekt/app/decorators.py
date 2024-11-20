from django.shortcuts import redirect

"""
def decorator(function):
    def wrap(request, *args, **kwargs):
        if SOMETHING:
            return function(request, *args, **kwargs)
        else:
            REJECT
    return wrap
"""

def professor_required(function):
    def wrap(request,*args, **kwargs):
        str_request = str(request.user.role).lower()

        if str_request == 'professor':
            return function(request,*args, **kwargs)
        else:
            if str_request =='admin':
                return redirect('main')
            else:
                return redirect('student')
            
    return wrap


def role_required(function, correct_role, another_role, first_url , second_url):
    def wrap(request,*args, **kwargs):
        str_request = str(request.user.role).lower()

        if str_request == correct_role:
            return function(request,*args, **kwargs)
        else:
            if str_request == another_role:
                return redirect(first_url)
            else:
                return redirect(second_url)
            
    return wrap

def professor_required(function):
    return role_required(function, 'professor', 'admin', 'main', 'student')

def admin_required(function):
    return role_required(function, 'admin', 'student', 'student', 'professor')

def student_required(function):
    return role_required(function, 'student', 'admin', 'main', 'professor')