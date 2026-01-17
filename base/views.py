# Import necessary modules
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message, User, Event
from .forms import RoomForm, UserForm, MyUserCreationForm

# View for handling login page
def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method =='POST':
        # Get email and password from the request
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        
        try:
            user= User.objects.get(username=email)
        except:
            messages.error(request, 'User does not exist')

        # Authenticate user
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            # Login user if authentication is successful
            login(request, user)
            return redirect('home')
        else: 
            messages.error(request,'Username OR Password is incorrect')
        
    context ={'page':page}
    return render(request, 'base/login_register.html', context)

# View for handling user logout
@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')

# View for handling user registration
def registerPage(request):
    form = MyUserCreationForm()

    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form': form})

# View for the home page
def home(request):
    return render(request, 'base/home.html')

# View for the team page
def team(request):
    return render(request, 'base/team.html')

# View for time management page
def timeManagement(request):
    return render(request, 'base/time_management.html')

# View for the calendar page
@login_required(login_url='login')
def calendar(request):
    user_events = Event.objects.filter(user=request.user)
    context = {
        "events": user_events,
    }
    return render(request, 'base/calendar.html', context)

# View for retrieving all events in JSON format
@login_required(login_url='login')
def all_events(request):
    user_events = Event.objects.filter(user=request.user)
    out = []
    for event in user_events:
        start = event.start.strftime("%m/%d/%Y, %H:%M:%S") if event.start else None
        end = event.end.strftime("%m/%d/%Y, %H:%M:%S") if event.end else None

        out.append({
            'title': event.name,
            'id': event.id,
            'start': start,
            'end': end,
            'complete': event.complete,
        })

    return JsonResponse(out, safe=False)

# View for adding a new event
@login_required(login_url='login')
def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    user = request.user
    event = Event(name=str(title), start=start, end=end, user=user)
    event.save()
    data = {}
    return JsonResponse(data)

# View for updating an existing event
@login_required(login_url='login')
def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    user = request.user
    event = get_object_or_404(Event, id=id, user=user)
    event.start = start
    event.end = end
    event.name = title
    event.save()
    data = {}
    return JsonResponse(data)

# View for removing an event
@login_required(login_url='login')
def remove(request):
    id = request.GET.get("id", None)
    user = request.user
    event = get_object_or_404(Event, id=id, user=user)
    event.delete()
    data = {}
    return JsonResponse(data)

# View for displaying the to-do list
@login_required(login_url='login')
def todoList(request):
    query = request.GET.get('q')
    user_tasks = Event.objects.filter(user=request.user).exclude(name__isnull=True, start__isnull=True, end__isnull=True)
    # If there is a search query, filter tasks based on the query
    if query:
        user_tasks = user_tasks.filter(
            Q(name__icontains=query) |  # Search by task name
            Q(start__icontains=query) |  # Search by start date 
            Q(end__icontains=query)  # Search by end date
        )
    return render(request, 'base/task_management.html', {'tasks': user_tasks, 'query': query})

# View for marking a task as complete
@login_required(login_url='login')
def complete_task(request, pk):
    user_event = get_object_or_404(Event, id=pk, user=request.user)
    user_event.complete = not user_event.complete  # Toggle completion status
    user_event.save()
    return redirect('tasks')

# View for deleting a task
@login_required(login_url='login')
def taskDelete(request, pk):
    task = Event.objects.get(id=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    return render(request, 'base/task_confirm_delete.html', {'task': task})

# View for handling forums
def forums(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/forums.html', context)

# View for handling individual rooms
def room(request, pk): 
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method =='POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    
    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)

# View for displaying user profile
def userPofile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)

# View for creating a new room
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
           description=request.POST.get('description'),
        )
        return redirect('forums')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)

# View for updating an existing room
@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method =='POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)

# View for deleting an existing room
@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!')
    
    if request.method == 'POST':
        room.delete()
        return redirect('forums')
    return render(request, 'base/delete.html', {'obj': room})

# View for deleting a message
@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!')
    
    if request.method == 'POST':
        message.delete()
        return redirect('forums')
    return render(request, 'base/delete.html', {'obj': message})

# View for updating user information
@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    return render(request, 'base/update_user.html', {'form': form})

# View for displaying topics
def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})

# View for displaying activity
def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})
