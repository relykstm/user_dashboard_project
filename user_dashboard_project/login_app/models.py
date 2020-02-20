from __future__ import unicode_literals
from django.db import models
import re
from time import strftime, localtime

class UserManager(models.Manager):
    def basic_validation(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first']) < 2:
            errors['first'] = "First name should be at least 2 characters."
        if len(postData['last']) < 2:
            errors['last'] = "Last name should be at least 2 characters."
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid Email."
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."
        if postData['password'] != postData['confirm']:
            errors['confirm'] = "Password and confirmed password did not match."
        if postData['date'] > strftime("%Y-%m-%d", localtime()):
            errors['date'] = "Birth date must be in the past."
        for each in User.objects.all():
            if each.email == postData['email']:
                errors['email'] = "Email already in our records."
        birth = postData['date']
        year, month, day = [int(f) for f in birth.split('-')]
        today = strftime("%Y-%m-%d", localtime())
        year2, month2, day2 = [int(f) for f in today.split('-')]
        if (year2 - year) < 13:
            errors['date'] = "You must be 13 years old to register(COPPA)"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birth = models.DateTimeField(null = True)
    updated_at = models.DateTimeField(auto_now = True)
    created_at = models.DateTimeField(auto_now_add = True)
    objects = UserManager()
    user_level = models.IntegerField(default=0)
    desc = models.TextField(default = "No description provided.")

class Message(models.Model):
    note = models.TextField()
    created_by2 = models.ForeignKey(User, related_name="messages_created", on_delete = models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(User, related_name="messages", on_delete = models.CASCADE)
    formatted_time = models.TextField(default = "99")

class Comment(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(User, related_name = "comments", on_delete = models.CASCADE)
    created_by2 = models.ForeignKey(User, related_name="comments_created", on_delete = models.CASCADE, default=1)
    message = models.ForeignKey(Message, related_name = "comments", on_delete = models.CASCADE)
