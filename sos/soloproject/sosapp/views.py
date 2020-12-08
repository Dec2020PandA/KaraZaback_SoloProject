from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    request.session.flush()
    return render(request, "index.html")

def register(request):
    if request.method == 'POST':
        errors = User.objects.reg_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()  
        new_user = User.objects.create(first_name=request.POST['first_name'], last_name= request.POST['last_name'], email=request.POST['email'], password= hashed_pw)  
        request.session['user_id'] = new_user.id
        request.session['greeting']=new_user.first_name
        return redirect('/events')
    return redirect('/')

def login(request):
    if request.method == 'POST':
        errors = User.objects.log_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        this_user = User.objects.get(email= request.POST['email'])
        request.session['user_id'] = this_user.id
        request.session['greeting']=this_user.first_name
        return redirect('/events')  
    return redirect('/')       

def logout(request):
    request.session.flush()
    return redirect('/')

def show_all(request):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        context = {
            "all_events": Event.objects.all()
        }
        return render(request, "show_all.html", context)

def new_event(request):
    if "user_id" not in request.session:
        return redirect('/')
    return render(request, "new.html")    

def create_event(request): 
    errors = Event.objects.event_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/events/new')
    else:
        event = Event.objects.create(name=request.POST['name'], description= request.POST['description'], attendees= request.POST['attendees'], date= request.POST['date'], time= request.POST['time'],creator=User.objects.get(id=request.session['user_id']))
    return redirect(f'/events/{event.id}')

def show_event(request, event_id):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        context = {
            "event": Event.objects.get(id=event_id)
        }
        return render(request, "show_event.html", context)

def show_user(request, user_id):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        context ={
            "user": User.objects.get(id=user_id)
        }
        return render(request, "show_user.html", context)
  

def edit_event(request, event_id):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        edit_event = Event.objects.filter(id=event_id)
        if len(edit_event) != 1:
            return redirect('/events')
        elif edit_event[0].creator.id != request.session['user_id']:
            return redirect('/events')    
        context = {
            'edit_event': edit_event[0]
        }    
        return render(request, 'edit.html', context)

def process_edit(request, event_id):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        event_edit = Event.objects.get(id=event_id)
        event_edit.item =request.POST['item'] 
        event_edit.save()
        return redirect('/events')   

def delete_event(request, event_id):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        Event.objects.get(id=event_id).delete()
        return redirect('/events')  

# def like(request, event_id):
#     liked_event = Event.objects.get(id=event_id)
#     user_liking = User.objects.get(id=request.session['user_id'])
#     liked_event.likes.add(user_liking) 
#     return redirect('/events')     

# def unlike(request, id):
#     liked_event = Event.objects.get(id=id)
#     user_liking = User.objects.get(id=request.session['user_id'])
#     liked_event.likes.remove(user_liking) 
#     return redirect('/events')


