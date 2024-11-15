from django.urls import path
from events.views import *
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', homepage, name='homepage'),
    path('register/', register, name='register'),
    path('events', event_list, name='event_list'),
    path('events/create/', event_create, name='event_create'),
    path('events/update/<int:pk>/', event_update, name='event_update'),
    path('events/delete/<int:pk>/', event_delete, name='event_delete'),
    path('events/<int:event_id>/rsvp/', rsvp_event, name='rsvp_event'),
    path('events/<int:event_id>/', event_detail, name='event_detail'),  # Add this line for event detail
    path('logout/',custom_logout, name='logout'),
    # Login and Logout URLs
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
