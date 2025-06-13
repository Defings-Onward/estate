from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from .models import Properties, Notification, visits, Application, services

def base(request):
    notification = Notification.objects.filter(recipient=request.user)
    return render(request, 'estate_mgt/base.html', context={
        'notification': notification
    })
def sign_up(request):
    message = "Pls sign up"
    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")
        username = request.POST.get("username")
        if password == password_confirm:
            user = User()
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.password = password
            group, created = Group.objects.get_or_create(name='agent')
            user.groups.add(group)
            user.save()

            
            
            login(request, user)
            print("signed in")
            return redirect('/')
        else:
            message = "Your Passwords don't match"
            print(message)
    else:
        message = "Your form was'nt submitted properly"
        print(message)

    return render(request, 'registration/signup.html', {"message": message})

def card(request):
    return render(request, "estate_mgt/card.html")
#@login_required(login_url="/login")
def home(request):
    properties = Properties.objects.filter(visible=True)[:5]
    notification = Notification.objects.filter(recipient=request.user.id)
    service = services.objects.all()
    context = {
        'properties': properties,
        'notification': Notification.objects.filter(recipient=request.user.id),
        'service': service
    }
    return render(request, 'estate_mgt/index.html', context=context)

def properties(request):
    properties = Properties.objects.all()
    group = Group.objects.get(name='agent')
    users = group.user_set.filter(username=request.user.username).first()
    print(users)
    context = {
        'properties': properties,
        'users': users,
        'notification': Notification.objects.filter(recipient=request.user.id),
    }
    return render(request, 'estate_mgt/properties.html', context=context)

@permission_required("estate_mgt.change_properties", raise_exception=True)
def manage_properties(request):
    properties = Properties.objects.all()
    if request.method == 'POST':
        btn_pty = request.POST.get("btn-pty")
        property = Properties.objects.filter(id=btn_pty).first()
        if property.visible == True:
            property.visible = False
            property.save()
            print("property unlisted")
            print(property.visible)
        elif property.visible == False and property.taken == False:
            property.visible = True
            property.save()
            print("property listed")
            print(property.visible)
    else:
        print("Form Was'nt clicked")

    context = {
        'properties': properties,
        'notification': Notification.objects.filter(recipient=request.user.id),

    }
    return render(request, 'estate_mgt/manage-properties.html', context=context)

@permission_required("estate_mgt.add_properties", raise_exception=True)
def create_property(request):
    if request.method == 'POST':
        details = request.POST.get("details")
        type = request.POST.get("type")
        location = request.POST.get("location")
        status = request.POST.get("status")
        area = request.POST.get("area")
        beds = request.POST.get("beds")
        baths = request.POST.get("baths")
        agent = request.POST.get("agent")
        price = request.POST.get("price")
        image = request.FILES.get("image")
        video = request.FILES.get("video")
        address = request.POST.get("address")
        property = Properties()
        property.details = details
        property.type = type
        property.location = location
        property.status = status
        property.area = area
        property.beds = beds
        property.baths = baths
        agentuser = User.objects.filter(username=agent).first()
        property.agent = agentuser
        def include_dot(a):
            amt = str(a)
            length = len(amt)
            value = ''
            arg = len(amt)%3
            if arg > 0:
                value += amt[0:arg] +'.'
            else:
                arg = 3
                value += amt[0:arg] + '.'

            cond = int((len(amt)-arg)/3)
        
            latest_prince = 0
            for x in range(0, cond+1):
                
                print(x)
                if x == 0:
                    latest_prince = arg-1
                if x != cond:
                    value += amt[latest_prince+1:latest_prince +4] + '.'
                    latest_prince += 3
            value = value[0:int(len(value))-1]
            return value
        property.price = include_dot(price)
        property.image = image
        property.address = address
        trying = str(video)
        print(trying)
        if trying[-3:] in ['mp4', 'webm', 'avi', 'mov', 'mkv'] or trying[-4:] in ['mp4', 'webm', 'avi', 'mov', 'mkv']:
            property.video = video
        else:
            print("Invalid file extension")
        
        property.save()

        
        print("Property Created!")
        return redirect('/manage-property')
    else:
        message = "Your form was'nt submitted properly"
        print(message)    
    group = Group.objects.get(name='agent')
    user = group.user_set.all()
    return render(request, 'estate_mgt/create-property.html', context={"users": user})

def property_single(request, id):
    property = Properties.objects.filter(id=id).first()
    taken = Application.objects.filter(property_id=id).first()
    if request.method == 'POST':
        date = request.POST.get("date")
        visit = visits()
        visit.sender = request.user
        visit.property = property
        visit.date = date
        

        notification = Notification()
        notification.head = "Visitation Alert"
        notification.body = f"Customer {request.user.username} has scheduled a visit \n for property {property.id} at {visit.date}"
        if request.user != property.agent:
            notification.recipient = property.agent
        else:
            notification.recipient = taken.client
        visit.save()
        notification.save()
        print("Visitation created")
    else:
        print("Eku ise.")
    return render(request, 'estate_mgt/property-single.html', context={'property': property,'notification': Notification.objects.filter(recipient=request.user.id),})
 
def service(request):
    service = services.objects.all()
    print(request.user.username)
    return render(request, 'estate_mgt/services.html', context={'service': service, 'notification': Notification.objects.filter(recipient=request.user.id),})

def service_detail(request,id):
    service = services.objects.all()
    service2 = services.objects.get(id=id)
    return render(request, 'estate_mgt/service-details.html', context={'services':service,'service':service2, 'notification': Notification.objects.filter(recipient=request.user.id),})

def contact(request):
    return render(request, 'estate_mgt/contact.html')

def about(request):
    return render(request, 'estate_mgt/about.html')

def agent(request):
    return render(request, 'estate_mgt/agents.html')
# Create your views here.
