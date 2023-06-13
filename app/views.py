from django.shortcuts import render,redirect
from .models import Course, Enrollment_list, User, Role
from django.http import HttpResponse
from .forms import Student_form,Professor_form,Course_form,Edit_user_form,Course_status_form
from django.db.models import Q
from django.db.models import Count, Sum
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from .decorators import admin_required
from django.shortcuts import get_object_or_404

# Create your views here.
def index(request):
    nickname = get_user(request)
    check = str(nickname)
    if check != 'AnonymousUser':
        name = nickname.first_name
        surname = nickname.last_name
        if name:
            return render(request,'index.html',{'name':name,'surname':surname})
        return render(request,'index.html',{'name':nickname})
    return render(request,'index.html',{'name':check})

@login_required
def all_courses(request):
    if request.user.role.role == Role.ADMIN:
        courses = Course.objects.all()
    elif request.user.role.role == Role.PROFESSOR:
        courses = Course.objects.filter(professor=request.user.id)
    else:
        return HttpResponse("Access Forbidden!")
    return render(request, 'all_courses.html', {"courses": courses})

@login_required   
@admin_required
def add_user(request, role):
    role=role.upper()

    if request.method == 'GET':
        if role == 'STUDENT':
            form = Student_form()

        elif role == 'PROFESSOR':
            form = Professor_form()

        return render(request, 'add_user.html', {'form': form, 'role': role})
    
    elif request.method == 'POST':
        if role == 'STUDENT':
            form = Student_form(request.POST)
            if form.is_valid():
                form.save()
                return redirect('all_students')
            else:
                return HttpResponse("FORM ERROR! ")
            
        elif role == 'PROFESSOR':
            form = Professor_form(request.POST)
            if form.is_valid():
                form.save()
                return redirect('all_professors')
            else:
                return HttpResponse("FORM ERROR!")

@login_required   
@admin_required
def add_course(request):
    if request.method == 'GET':
        form = Course_form()
        return render(request, 'add_course.html', {'form': form})
    elif request.method == 'POST':
        form = Course_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_courses')
        else:
            return HttpResponse("FORM ERROR")
        
@login_required   
@admin_required         
def edit_course(request,id):
    course = Course.objects.get(id=id)
    if request.method == 'GET':
        form = Course_form(instance=course)
        return render(request, 'edit_course.html', {'form': form})
    elif request.method == 'POST':
        form = Course_form(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('all_courses')
        else:
            return HttpResponse("FORM ERROR")



@login_required   
@admin_required  
def edit_user(request,id):
    user = User.objects.get(id=id)
    if request.method == 'GET':
        form = Edit_user_form(instance=user)
        return render(request, 'edit_user.html', {'form': form})
    elif request.method == 'POST':
        form = Edit_user_form(request.POST,instance=user)
        if form.is_valid():
            form.save()
            if user.role.role == Role.STUDENT:
                return redirect('all_students')
            else:
                return redirect('all_professors')
        else:
            return HttpResponse("FORM ERROR")
        

@login_required   
@admin_required  
def delete_user(request,id):
    user = User.objects.get(id=id)
    user.delete() 
    if user.role.role == Role.STUDENT:
        return redirect('all_students')
    elif user.role.role == Role.PROFESSOR:
        return redirect('all_professors')
    
    
@login_required   
@admin_required  
def delete_course(request,id):
    course = Course.objects.get(id=id)
    course.delete() 
    return redirect('all_courses')

@login_required
def students_on_course(request, id):
    course = Course.objects.get(id=id)
    if request.user.role.role == 'ADMIN' or request.user.role.role == 'PROFESSOR' and request.user == course.professor:
        enrollment_record = Enrollment_list.objects.filter(course=course)
        enrollment_record_np=Enrollment_list.objects.filter(course=course, status='nepolozen')
        enrollment_record_p=Enrollment_list.objects.filter(course=course, status='polozen')
        enrollment_record_dp=Enrollment_list.objects.filter(course=course, status='upisan')
        context={'enrollment_record': enrollment_record, 'course': course,'enrollment_record_np':enrollment_record_np,'enrollment_record_p':enrollment_record_p,'enrollment_record_dp':enrollment_record_dp}
        return render(request,'students_on_course.html', context)
    return redirect('all_courses')


@admin_required
@login_required
def all_professors(request):
    professors = User.objects.filter(role_id__role=Role.PROFESSOR)
    return render(request, 'all_professors.html', {"professors": professors})


@login_required
def all_students(request):
    if request.user.role.role == Role.ADMIN or request.user.role.role == Role.PROFESSOR:
        students = User.objects.filter(role_id__role=Role.STUDENT)
        return render(request, 'all_students.html', {"students": students})
    else:
        return HttpResponse("Access Denied!")
    

@login_required
def enrollment_list(request, student_id):
    if request.user.role.role == Role.ADMIN or (request.user.role.role == Role.STUDENT and request.user.id == student_id):
        try:
            student = User.objects.get(id=student_id)
        except User.DoesNotExist:
            return HttpResponse("Access Denied! User does not exist!")

        enrollment_record_course_ids = Enrollment_list.objects.filter(student=student).values_list('course_id', flat=True)
        available_courses = Course.objects.exclude(id__in=enrollment_record_course_ids)

        enrollment_record_block_disenroll_ids = Enrollment_list.objects.filter(
            Q(status="polozen") | Q(status="nepolozen"), student=student
        ).values_list('course_id', flat=True)
        block_disenroll_courses = Course.objects.exclude(~Q(id__in=enrollment_record_block_disenroll_ids)).order_by('id')

        if student.status == 'redovni student':
            enrolled_courses = Course.objects.exclude(~Q(id__in=enrollment_record_course_ids)).order_by('id')
        else:
            enrolled_courses = Course.objects.exclude(~Q(id__in=enrollment_record_course_ids)).order_by('semester_pt', 'id')

        total_ects = Enrollment_list.objects.filter(student=student).aggregate(total_ects=Sum('course__ects'))['total_ects'] or 0
        total_ects_passed = Enrollment_list.objects.filter(student=student, status='polozen').aggregate(total_ects_passed=Sum('course__ects'))['total_ects_passed'] or 0

        courses_enrolled = Enrollment_list.objects.filter(student=student, status='upisan').count()
        courses_passed = Enrollment_list.objects.filter(student=student, status='polozen').count()
        courses_lost_signature = Enrollment_list.objects.filter(student=student, status='nepolozen').count()
    else:
        return HttpResponse("Access Denied!")

    context = {
        'student': student,
        'available_courses': available_courses,
        'enrolled_courses': enrolled_courses,
        'block_disenroll_courses': block_disenroll_courses,
        'total_ects': total_ects,
        'total_ects_passed': total_ects_passed,
        'courses_enrolled': courses_enrolled,
        'courses_passed': courses_passed,
        'courses_lost_signature': courses_lost_signature,
    }
    return render(request, 'enrollment_list.html', context)

@login_required
def enroll_course(request, student_id, course_id):
    user = request.user

    if user.role.role == Role.ADMIN or (user.role.role == Role.STUDENT and user.id == student_id):
        student = get_object_or_404(User, id=student_id)
        course = get_object_or_404(Course, id=course_id)

        Enrollment_list.objects.create(student=student, course=course)
    else:
        return HttpResponse("ERROR! Access Denied!")

    return redirect('enrollment_list', student_id)



@login_required
def disenroll_course(request, student_id, course_id):
    user = request.user
    
    if user.role.role == Role.ADMIN or (user.role.role == Role.STUDENT and user.id == student_id):
        enrollment_record = get_object_or_404(Enrollment_list, student_id=student_id, course_id=course_id)
        
        if enrollment_record.status == 'upisan':
            enrollment_record.delete()
        elif enrollment_record.status == 'polozen':
            return HttpResponse("ERROR! Action Not Possible!")
        else:
            return HttpResponse("ERROR! Action Not Possible!")
    else:
        return HttpResponse("ERROR! Access Denied!")
    
    return redirect('enrollment_list', student_id)

@login_required
def change_course_status(request, id):
    user = request.user
    
    enrollment_list = Enrollment_list.objects.get(id=id)
    course = enrollment_list.course
    
    if user.role.role == Role.ADMIN or (user.role.role == Role.PROFESSOR and user == course.professor):
        if request.method == 'GET':
            form = Course_status_form(instance=enrollment_list)
            return render(request, 'change_course_status.html', {'form': form, 'list': enrollment_list})
        elif request.method == 'POST':
            form = Course_status_form(request.POST, instance=enrollment_list)
            
            if form.is_valid():
                form.save()
                return redirect('students_on_course', course.id)
            else:
                return HttpResponse("FORM ERROR")
    else:
        return HttpResponse("ERROR! Access Denied!")