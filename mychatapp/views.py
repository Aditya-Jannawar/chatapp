from django.shortcuts import render, redirect
from .models import ChatMessage, Profile, Friend
from .forms import ChatMessageForm, ProfileForm
from django.http import JsonResponse
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import CustomPasswordChangeForm
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    user = request.user.profile
    friends = user.friends.all()
    context = {"user": user, "friends": friends}
    return render(request, "mychatapp/index.html", context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'mychatapp/login.html', {'error_message': error_message})
    else:
        return render(request, 'mychatapp/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def detail(request, pk):
    friend = Friend.objects.get(profile_id=pk)
    user = request.user.profile
    profile = Profile.objects.get(id=friend.profile.id)
    chats = ChatMessage.objects.all()
    rec_chats = ChatMessage.objects.filter(
        msg_sender=profile, msg_receiver=user, seen=False)
    rec_chats.update(seen=True)
    form = ChatMessageForm()
    if request.method == "POST":
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.msg_sender = user
            chat_message.msg_receiver = profile
            chat_message.save()
            return redirect("detail", pk=friend.profile.id)
    context = {"friend": friend, "form": form, "user": user,
               "profile": profile, "chats": chats, "num": rec_chats.count()}
    return render(request, "mychatapp/detail.html", context)


def sentMessages(request, pk):
    user = request.user.profile
    friend = Friend.objects.get(profile_id=pk)
    profile = Profile.objects.get(id=friend.profile.id)
    data = json.loads(request.body)
    new_chat = data["msg"]
    new_chat_message = ChatMessage.objects.create(
        body=new_chat, msg_sender=user, msg_receiver=profile, seen=False)
    print(new_chat)
    return JsonResponse(new_chat_message.body, safe=False)


def receivedMessages(request, pk):
    user = request.user.profile
    friend = Friend.objects.get(profile_id=pk)
    profile = Profile.objects.get(id=friend.profile.id)
    arr = []
    chats = ChatMessage.objects.filter(msg_sender=profile, msg_receiver=user)
    for chat in chats:
        arr.append(chat.body)

    return JsonResponse(arr, safe=False)


def chatNotification(request):
    user = request.user.profile
    friends = user.friends.all()
    arr = []
    for friend in friends:
        chats = ChatMessage.objects.filter(
            msg_sender__id=friend.profile.id, msg_receiver=user, seen=False)
        arr.append(chats.count())
    return JsonResponse(arr, safe=False)


def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES,
                           instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, "mychatapp/edit_profile.html", {'form': form})


@login_required
def change_password(request):
    user = request.user.profile
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request, 'Your password was successfully updated!')
            update_session_auth_hash(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, "mychatapp/change_password.html", {'form': form, "user": user})
