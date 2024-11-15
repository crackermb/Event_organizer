# from django.shortcuts import render, redirect, get_object_or_404
# from .forms import UserRegistrationForm, EventForm, RSVPForm
# from django.contrib.auth.decorators import login_required
# from .models import Event, RSVP
# from .models import UserProfile
# from django.core.mail import send_mail

# # User Registration View
# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             return redirect('login')
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'register.html', {'form': form})
# # Event List View
# def event_list(request):
#     events = Event.objects.all()
#     return render(request, 'event_list.html', {'events': events})

# # Event Create View
# @login_required
# def event_create(request):
#     if request.method == 'POST':
#         form = EventForm(request.POST)
#         if form.is_valid():
#             event = form.save(commit=False)
#             event.organizer = request.user  # Ensure the user is authenticated
#             event.save()
#             return redirect('event_list')
#     else:
#         form = EventForm()
#     return render(request, 'event_form.html', {'form': form})
# # Event Update View
# def event_update(request, pk):
#     event = get_object_or_404(Event, pk=pk)
#     if request.method == 'POST':
#         form = EventForm(request.POST, instance=event)
#         if form.is_valid():
#             form.save()
#             return redirect('event_list')
#     else:
#         form = EventForm(instance=event)
#     return render(request, 'event_form.html', {'form': form})

# # Event Delete View
# def event_delete(request, pk):
#     event = get_object_or_404(Event, pk=pk)
#     event.delete()
#     return redirect('event_list')

# # RSVP Event View
# @login_required
# def rsvp_event(request, event_id):
#     event = get_object_or_404(Event, id=event_id)

#     try:
#         rsvp = RSVP.objects.get(event=event, user=request.user)
#     except RSVP.DoesNotExist:
#         rsvp = None

#     if request.method == 'POST':
#         form = RSVPForm(request.POST, instance=rsvp)
#         if form.is_valid():
#             rsvp = form.save(commit=False)
#             rsvp.event = event
#             rsvp.user = request.user
#             rsvp.save()
#             return redirect('event_list')  # Redirect to event list after RSVP
#     else:
#         form = RSVPForm(instance=rsvp)

#     return render(request, 'rsvp_event.html', {'event': event, 'form': form})

# def event_detail(request, event_id):
#     event = get_object_or_404(Event, id=event_id)
#     return render(request, 'event_detail.html', {'event': event})
# # Homepage Redirect View
# def homepage(request):
#     return redirect('event_list')
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, EventForm, RSVPForm
from django.contrib.auth.decorators import login_required
from .models import Event, RSVP, UserProfile
from django.core.mail import send_mail
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth import logout

# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # You could send a welcome email after successful registration
            send_mail(
                'Welcome to Event Manager!',
                f"Hi {user.username}, thanks for registering with us!",
                'from@example.com',
                [user.email],
                fail_silently=False,
            )
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


# Event List View
def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})


# Event Create View with Email Notifications for Users with Matching Interests
@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user  # Ensure the user is authenticated
            event.save()

            # Find users whose interests match the event category
            interested_users = UserProfile.objects.filter(interests__icontains=event.category)

            # Send email to each interested user
            for profile in interested_users:
                send_mail(
                    f"New Event: {event.title} might interest you!",
                    f"Hi {profile.user.username},\n\nA new event titled '{event.title}' might match your interests. Check it out on {event.date}.",
                    'from@example.com',
                    [profile.user.email],
                    fail_silently=False,
                )

            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'event_form.html', {'form': form})

def custom_logout(request):
    logout(request)  # Clears the session
    return redirect('event_list')  # Redirect after logout
# Event Update View
@login_required
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'event_form.html', {'form': form})


# Event Delete View
@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.delete()
    return redirect('event_list')


# RSVP Event View with Confirmation Email
@login_required
def rsvp_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    try:
        rsvp = RSVP.objects.get(event=event, user=request.user)
    except RSVP.DoesNotExist:
        rsvp = None

    if request.method == 'POST':
        form = RSVPForm(request.POST, instance=rsvp)
        if form.is_valid():
            rsvp = form.save(commit=False)
            rsvp.event = event
            rsvp.user = request.user
            rsvp.save()

            # Send RSVP confirmation email
            send_mail(
                f"RSVP Confirmation for {event.title}",
                f"Hi {request.user.username},\n\nYou have successfully RSVP'd as '{rsvp.get_status_display()}' for the event '{event.title}' happening on {event.date}.",
                'from@example.com',
                [request.user.email],
                fail_silently=False,
            )

            return redirect('event_list')  # Redirect to event list after RSVP
    else:
        form = RSVPForm(instance=rsvp)

    return render(request, 'rsvp_event.html', {'event': event, 'form': form})


# Event Detail View
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_detail.html', {'event': event})


# Homepage Redirect View (to event list)
def homepage(request):
    return redirect('event_list')


# Task for sending reminders to users 1 day before the event
def send_event_reminders(request):
    upcoming_events = Event.objects.filter(date__gte=timezone.now())

    for event in upcoming_events:
        # Get users who RSVP'd to the event
        rsvps = RSVP.objects.filter(event=event, status='going')

        for rsvp in rsvps:
            # Send a reminder email
            send_mail(
                f"Reminder: {event.title} is happening soon!",
                f"Hi {rsvp.user.username},\n\nDon't forget about the event {event.title} happening on {event.date} at {event.location}. We hope to see you there!",
                'from@example.com',
                [rsvp.user.email],
                fail_silently=False,
            )

    return HttpResponse("Reminders sent!")  # This is just for testing; in production, you'd use a task scheduler like Celery
