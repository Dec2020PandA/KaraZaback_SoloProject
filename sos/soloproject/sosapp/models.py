from django.db import models
import re
import bcrypt
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.

class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        if len(postData['first_name'])== 0:
            errors['first_name']="First name is required!!"
        elif len(postData['first_name'])<2 or postData['first_name'].isalpha() != True:
            errors['first_name'] = "First name must be at least 2 characters long, letters only!!"   
        
        if len(postData['last_name'])==0:
            errors['last_name']="Last name is required!!"
        elif len(postData['last_name'])<2 or postData['last_name'].isalpha() != True:
            errors['last_name'] = "Last name must be at least 2 characters long, letters only!!"     
        
        if len(postData['email'])==0:
            errors['email']="Email is required!!"
        elif not email_regex.match(postData['email']):
           errors['email']="Email must be vaild format!!"
        existing_user = User.objects.filter(email=postData['email'])
        if len(existing_user)!=0:
            errors['email'] = "Email already in use"   
        
        if len(postData['password'])==0:
            errors['password']="Password is required!!"   
        elif len(postData['password'])<8:
            errors['password']="Your password must be more than 8 Characters!!"
        if postData['password'] != postData['confirm_pw']:
            errors['confirm_password'] = "Password and confirm password do not match!!"
        return errors

    def log_validator(self, postData):
        errors = {}
        if len(postData['email'])==0:
            errors['email']="Email is required!!"
        elif not email_regex.match(postData['email']):
           errors['email']="Email must be vaild format!!"
        existing_user = User.objects.filter(email=postData['email'])
        if len(existing_user)!=1:
            errors['email'] = "User not found"   
        
        if len(postData['password'])==0:
            errors['password']="Password is required!!"   
        elif len(postData['password'])<8:
            errors['password']="Your password must be more than 8 Characters!!"
        elif bcrypt.checkpw(postData['password'].encode(), existing_user[0].password.encode()) != True:
            errors['email'] = "Email and password do not match"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=UserManager()

class EventManager(models.Manager):
    def event_validator(self, postData):
        errors = {}
        if len(postData['name'])== 0:
            errors['name']="Event Name is required!!"
        elif len(postData['name'])<2:
            errors['name'] = "Your event name must be at least 2 characters long!!"   
        
        if len(postData['description'])== 0:
            errors['description']="A description is required!!"
        elif len(postData['description'])<2:
            errors['description'] = "Your description must be at least 2 characters long!!"
        
        if len(postData['attendees'])== 0:
            errors['attendees']="Number of attendees is required!!"
        # /elif len(postData['attendees'])<10:
        #     errors['attendees'] = "Must be atleast 10 attendees!!"    
        
        if len(postData['date'])== 0:
            errors['date']="Date is required!!"

        # if len(postData['date'])== 0:
        #     errors['date']="A date is required!!"
        # # elif len(postData['date'])<2:
        # #     errors['date'] = "Your date must be at least 2 characters long!!"
        

        return errors

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    attendees = models.IntegerField(max_length=100)
    # date = date.strptime(date_string, "YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]")
    date = models.DateTimeField(null=True, blank=True)
    join = models.BooleanField(default=False)
    creator = models.ForeignKey(User, related_name="event_list", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True) 
    objects=EventManager()