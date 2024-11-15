from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    interests = models.TextField()  # Interests to suggest relevant events
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
    
class Event(models.Model):
    CATEGORY_CHOICES = [
        ('SOC', 'Social'),
        ('EDU', 'Educational'),
        ('REC', 'Recreational'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=255)
    date = models.DateTimeField()
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

from django.db import models
from django.contrib.auth.models import User
from .models import Event  # Assuming Event is in the same models.py or imported

class RSVP(models.Model):
    STATUS_CHOICES = (
        ('going', 'Going'),
        ('interested', 'Interested'),
        ('not_going', 'Not Going'),
    )

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')  # Ensure one RSVP per user per event

    def __str__(self):
        return f"{self.user.username} - {self.event.title} - {self.status}"

################################################
# models.py (Reminder email function)

from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta

def send_event_reminder(event):
    # Fetch RSVPs where the user is 'going'
    attendees = RSVP.objects.filter(event=event, status='going')

    for rsvp in attendees:
        user = rsvp.user
        send_mail(
            subject=f'Reminder: {event.title} is happening soon!',
            message=f'Hi {user.username},\n\nThis is a reminder that the event "{event.title}" is happening on {event.date}. We hope to see you there!\n\nBest regards,\nEvent Organizer Team',
            from_email='your_email@example.com',
            recipient_list=[user.email],  # This gets the email from the User model
            fail_silently=False,
        )
