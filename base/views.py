# from multiprocessing import context
# from pydoc_data.topics import topics
import datetime
from distutils.command.upload import upload
from email import message
import email
from math import fabs
from multiprocessing import context
from pydoc_data.topics import topics
from re import X
from unicodedata import name
from venv import create
from django import shortcuts
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
# from matplotlib.style import context
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from .models import Message, Room, Topic, User, BMS
from .forms import RoomForm, UserForm, MyUserCreationForm, WarrantyForm
from .functionX import MyFunction, function2, functionTest
from .funcBMS import *
import time
# from django.views.decorators.csrf import csrf_exempt,csrf_protect

# Create your views here.

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')

    context = {'page':page}
    return render(request, 'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = MyUserCreationForm()
    page = 'register'
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'An error occured during registration!')

    return render(request,'base/login_register.html',{'form':form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q) | Q(role__icontains=q))
        
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id = pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body'),
            images = request.FILES.get('images'),
            file = request.FILES.get('files')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
                'participants': participants}
    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user,'rooms':rooms,'room_messages': room_messages,'topics':topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            product_serial_number = request.POST.get('product_serial_number'),
            product_model = request.POST.get('product_model'),
            date_of_installation = request.POST.get('date_of_installation'),
            company = request.POST.get('company'),
            contact_person = request.POST.get('contact_person'),
            contact_number = request.POST.get('contact_number'),
            email = request.POST.get('email'),
            other_recipients = request.POST.get('other_recipients'),
            site_address = request.POST.get('site_address'),
            shipping_address = request.POST.get('shipping_address'),
            description = request.POST.get('description')
        )
        if str(topic) == 'Bảo hành inverter': #send mail here
            functionTest()
        #form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     form.save()
        return redirect('home')

    context = {'form': form, 'topics':topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('<h1>You are not allowed here!</h1>')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid:
            form.save()
            return redirect('room', pk=room.id)

    context = {'form': form, 'topics':topics}
    return render(request, 'base/room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('<h1>You are not allowed here!</h1>')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse('<h1>You are not allowed here!</h1>')

    try:
        room = Room.objects.get(id=pk)
        if request.method == 'POST':
            message.delete()
            return redirect('room', pk=room.id)
    except:
        if request.method == 'POST':
            message.delete()
            return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    context = {'form':form}

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile', pk=user.id)

    return render(request,'base/update-user.html' , context)

def topicPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context={'topics':topics}
    return render(request, 'base/topics.html',context)

def activityPage(request):
    room_messages = Message.objects.all()
    context = {'room_messages': room_messages}
    return render(request, 'base/activity.html', context)

@login_required(login_url='login')
def warrantyForm(request):
    form = WarrantyForm()
    if request.method == 'POST':
        product_serial_number = request.POST.get('product_serial_number')
        product_model = request.POST.get('product_model')
        date_of_installation = request.POST.get('date_of_installation')
        company = request.POST.get('company')
        contact_person = request.POST.get('contact_person')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')
        other_recipients = request.POST.get('other_recipients')
        site_address = request.POST.get('site_address')
        shipping_address = request.POST.get('shipping_address')
        
        MyFunction(product_serial_number,product_model,date_of_installation,company,contact_person,contact_number,email,other_recipients,site_address,shipping_address)

        return redirect('home')
    
    context = {'form': form}
    return render(request, 'base/warranty_form.html', context)

@login_required(login_url='login')
def roomRole(request, pk):
    room = Room.objects.get(id=pk)

    # if request.user != room.host:
    #     return HttpResponse('<h1>You are not allowed here!</h1>')

    if request.method == 'POST':
        if room.role<6:
            room.role = room.role + 1
            room.save()
            # print('here: ',str(room.created))
            return redirect('room', pk=room.id)
        else:
            return redirect('room', pk=room.id)
    return render(request, 'base/room-role.html', {'obj':room.role})

def bms(request, pk):
    user = User.objects.get(id=pk)
    bms = BMS.objects.all()

    try:
        data90 = get_data(pk,'90')
        total_vol = data90[0]
        gather_vol = data90[1]
        current = data90[2]
        soc = data90[3]
        # print("here: ",data90)

        data91 = get_data(pk,'91')
        max_cell_vol = data91[0]
        no_of_max = data91[1]
        min_cell_vol = data91[2]
        no_of_min = data91[3]
        # print("here: ",data91)

        data93 = get_data(pk,'93')
        state = data93[0]
        remain_cap = data93[4]
    except:
        total_vol = 0
        gather_vol = 0
        current =0
        soc = 0
        # print("here: ",data90)

        max_cell_vol = 0
        no_of_max = 0
        min_cell_vol = 0
        no_of_min = 0
        # print("here: ",data91)

        state = 0
        remain_cap = 0
    # print("here: ",data91)

    context = {'remain_cap':remain_cap,'state':state,'user': user,'bms':bms, 'total_vol': total_vol, 'gather_vol':gather_vol, 'current':current,'soc':soc, 'max_cell_vol':max_cell_vol,'no_of_max':no_of_max,'min_cell_vol':min_cell_vol,'no_of_min':no_of_min}
    return render(request, 'base/bms.html', context)

def bmsDetail(request, pk):
    user = User.objects.get(id=pk)
    bms = BMS.objects.all()

    a = [0,0,0,0]
    total_vol = a[0]
    gather_vol = a[1]
    current = a[2]
    soc = a[3]
    print("here: ",a)


    context = {'user': user,'bms':bms, 'total_vol': total_vol, 'gather_vol':gather_vol, 'current':current,'soc':soc}
    return render(request, 'base/bmsDetail.html', context)