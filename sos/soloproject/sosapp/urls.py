from django.urls import path
from . import views

urlpatterns = [
    path('', views.index), #GET
    path('register', views.register),#POST
    path('login', views.login),#POST
    path('logout', views.logout),#GET/POST
    path('events', views.show_all),#GET
    path('events/new', views.new_event),#GET
    path('events/<int:event_id>', views.show_event),#GET
    path('events/create', views.create_event),#POST
    path('events/edit/<int:event_id>', views.edit_event),#POST
    path('process_edit/<int:event_id>', views.process_edit),
    path('events/delete/<int:event_id>', views.delete_event),#POST
    # path('events/<int:event_id>/like', views.like),#POST
    # path('events/<int:event_id>/unlike', views.unlike),#POST
    path('users/<int:event_id>', views.show_user),#GET
    path('events/join/<int:event_id>', views.join),
]