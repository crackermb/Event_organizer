# tasks.py (New File)

from django.utils import timezone
from django.core.mail import send_mail
from .models import Event, RSVP

def send_event_reminders():
    upcoming_events = Event.objects.filter(date__gte=timezone.now())  # Get upcoming events

    for event in upcoming_events:
        # Get users who RSVP'd to the event
        rsvps = RSVP.objects.filter(event=event, status='going')

        for rsvp in rsvps:
            # Send a reminder email
            send_mail(
                f"Reminder: {event.title} is happening soon!",
                f"Hi {rsvp.user.username},\n\nDon't forget about the event {event.title} happening on {event.date} at {event.location}. We hope to see you there!",
                'mehulbhatia@example.com',
                [rsvp.user.email],
                fail_silently=False,
            )
