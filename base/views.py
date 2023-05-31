from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from .models import *
from .forms import *

# Create your views here.
@csrf_protect
def search_room(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest': #check is Ajax
        if request.POST.get('room'):
            query = request.POST.get('room')
            rooms = Room.objects.filter(
                Q(topic__name__icontains=query) |
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )
            if rooms:
                data = []
                for room in rooms:
                    data.append({
                        'id': room.id,
                        'name': room.name
                    })
            else:
                data = "No room found..."
            return JsonResponse({'data': data})
    return JsonResponse({})


def home(request):
    if request.GET.get('q'):
        q = request.GET.get('q')
        rooms = Room.objects.filter(
            Q(topic__name__icontains=q) |
            Q(name__icontains=q) |
            Q(description__icontains=q)
            )
        room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    else:
        topic_req = request.GET.get('topic') if request.GET.get('topic') else ''
        rooms = Room.objects.filter(topic__name__contains=topic_req)
        room_messages = Message.objects.filter(Q(room__topic__name__contains=topic_req)).order_by('-created')[:5]
    room_count = rooms.count()
    topics = Topic.objects.all()
    context = {'rooms': rooms,
               'topics': topics,
               'room_count': room_count,
               'room_messages': room_messages,}
    return render(request, 'base/home.html', context)


def room(request, pk):
    try:
        room = Room.objects.get(id=pk)
    except:
        return HttpResponse("Room does not exist.")
    
    if request.method == "POST":
        new_message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    
    participants = room.participants.all()
    room_messages = room.message_set.all().order_by('-created')
    context = {'room': room,
               'room_messages': room_messages,
               'participants': participants}
    return render(request, 'base/room.html', context)


def profile(request, pk):
    profile_user = User.objects.get(id=pk)
    topics = Topic.objects.all()
    rooms = Room.objects.filter(Q(host=profile_user))
    room_messages = Message.objects.filter(Q(user=profile_user))
    
    context = {
        'profile_user': profile_user,
        'topics': topics,
        'rooms': rooms,
        'room_messages': room_messages,
        'page': 'profile',
    }

    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
@csrf_protect
def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
@csrf_protect
def updateRoom(request, pk):
    try:
        room = Room.objects.get(id=pk)
    except:
        return redirect('home')
    form = RoomForm(instance=room)

    if request.user != room.host:
        messages.warning(request, "You must be host to update room.")
        return redirect('home')

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form": form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
@csrf_protect
def deleteRoom(request, pk):
    try:
        room = Room.objects.get(id=pk)
    except:
        return redirect('home')

    if request.user != room.host:
        return HttpResponse("You must be host to delete room.")

    if request.method == "POST":
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url='login')
@csrf_protect
def deleteMessage(request, pk):
    try:
        message = Message.objects.get(id=pk)
    except:
        return redirect('home')

    if request.user != message.user:
        return HttpResponse("Cannot delete this message.")

    if request.method == "POST":
        msg_id = message.room.id
        message.delete()
        return redirect('room', pk=msg_id)

    return render(request, 'base/delete.html', {'obj': message})

@csrf_protect
def userLogin(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password is not correct.")

    context = {'page': 'login'}

    return render(request, 'base/login_register.html', context)

@csrf_protect
def userRegister(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            return redirect('home')
        else:
            messages.error(request, "Error occurs during registration.")

    context = {'form': UserCreationForm}
    return render(request, 'base/login_register.html', context)

@login_required(login_url='login')
def userLogout(request):
    logout(request)
    return redirect('home')