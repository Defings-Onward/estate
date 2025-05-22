from django.shortcuts import render
from .models import Appointments, Doctor, Department
from django.contrib.auth.models import User

def home(request):
    departments = Department.objects.all()
    doctors = Doctor.objects.all()
    department_no = departments.count()
    doctor_no = doctors.count()
    if request.method == 'POST':
        username = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        date = request.POST.get("date")
        department = request.POST.get("department")
        doctor = request.POST.get("doctor")
        print("doctor:", doctor)
        message = request.POST.get("message")
        try:
            user = User.objects.get(username=username)
        except:
            User.objects.create(username=username,email=email,password=phone)
            user = User.objects.get(username=username)
        appointments = Appointments()
        appointments.patient = user
        appointments.date = date
        depart_ment = Department.objects.get(name=department)
        appointments.department = depart_ment
        doctor_user = User.objects.get(username=doctor)
        doc_tor = Doctor.objects.get(user=doctor_user)
        appointments.doctor = doc_tor
        appointments.message = message
        appointments.save()

    print(department_no)

    context = {
        'departments': departments,
        'doctors': doctors,
        'doctor_no': doctor_no,
        'department_no': department_no
    }
    return render(request, 'index.html', context=context)
# Create your views here.
