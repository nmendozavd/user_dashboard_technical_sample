# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import date
import datetime
from time import strftime
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASS_REGEX = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$")

class UserManager(models.Manager):
    def ageValidator(self, postData):
        try:
            dob = postData['dob']
            date_of_birth = dob.replace("-","")
            year = datetime.datetime.now().year
            dob = int(date_of_birth) / 10000
            if (year - dob) < 5 or (year - dob) > 123:
                return False
        except:
            return False
        return True

    def validateRegistration(self, postData):
        response = {}
        if len(postData['first_name']) < 1 or len(postData['last_name']) < 1 or len(postData['email']) < 1 or len(postData['username']) < 1 or len(postData['password']) < 1:
            try:
                response['error'].append("Please fill in all fields")
            except:
                response['error'] = []
                response['error'].append("Please fill in all fields")
        if not postData['first_name'].isalpha() or not postData['last_name'].isalpha() or len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
            try:
                response['error'].append("Please enter a valid name")
            except:
                response['error'] = []
                response['error'].append("Please enter a valid name")
        if not User.objects.ageValidator(postData):
            try:
                response['error'].append("Please enter a valid date of birth")
            except:
                response['error'] = []
                response['error'].append("Please enter a valid date of birth")
        if not EMAIL_REGEX.match(postData['email']):
            try:
                response['error'].append("Please enter a valid email address")
            except:
                response['error'] = []
                response['error'].append("Please enter a valid email address")
        if postData['password'] != postData['confirm_password']:
            try:
                response['error'].append("Password and Confirm Password must match")
            except:
                response['error'] = []
                response['error'].append("Password and Confirm Password must match")
        if not PASS_REGEX.match(postData['password']):
            try:
                response['error'].append("Passwords must be at least 8 characters, including 1 lowercase, 1 uppercase, 1 special character, and 1 number")
            except:
                response['error'] = []
                response['error'].append("Passwords must be at least 8 characters, including 1 lowercase and 1 number")
        db_email_check = User.objects.filter(email = postData['email'])
        if len(db_email_check) > 0:
            try:
                response['error'].append("Email is already registered")
            except:
                response['error'] = []
                response['error'].append("Email is already registered")
        db_username_check = User.objects.filter(username = postData['username'])
        if len(db_username_check) > 0:
            try:
                response['error'].append("Username is already taken")
            except:
                response['error'] = []
                response['error'].append("Username is already taken")
        return response
    
    def addUser(self, postData):
        password = postData['password']
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        newuser = User.objects.create(first_name = postData['first_name'], last_name = postData['last_name'], email = postData['email'], username = postData['username'], date = postData['dob'], password = hashed_pw)
        return newuser

    def validateLogin(self, postData):
        check_login_em = User.objects.filter(email = postData['user_input'])
        if len(check_login_em) < 1:
            check_login_us = User.objects.filter(username = postData['user_input'])
            if len(check_login_us) < 1:
                return False
        input_password = postData['password']
        try: 
            retrieved_pass = User.objects.get(username = postData['user_input']).password
        except:
            retrieved_pass = User.objects.get(email = postData['user_input']).password
        if not bcrypt.checkpw(input_password.encode(), retrieved_pass.encode()):
            return False
        else:
            try:
                user_id = User.objects.get(username = postData['user_input']).id
            except:
                user_id = User.objects.get(email = postData['user_input']).id
            return user_id

    def validateEdit(self, postData, user_id):
        response = {}
        if len(postData['first_name']) < 1 or len(postData['last_name']) < 1 or len(postData['email']) < 1 or len(postData['username']) < 1:
            try:
                response['error'].append("Please don't leave any fields blank")
            except:
                response['error'] = []
                response['error'].append("Please don't leave any fields blank")
        if not postData['first_name'].isalpha() or not postData['last_name'].isalpha() or len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
            try:
                response['error'].append("Please enter a valid name")
            except:
                response['error'] = []
                response['error'].append("Please enter a valid name")
        if not EMAIL_REGEX.match(postData['email']):
            try:
                response['error'].append("Please enter a valid email address")
            except:
                response['error'] = []
                response['error'].append("Please enter a valid email address")
        other_emails = User.objects.exclude(id = user_id)
        db_email_check = other_emails.filter(email = postData['email'])
        if len(db_email_check) > 0:
            try:
                response['error'].append("Email is already registered")
            except:
                response['error'] = []
                response['error'].append("Email is already registered")
        other_usernames = User.objects.exclude(id = user_id)
        db_username_check = other_usernames.filter(username = postData['username'])
        if len(db_username_check) > 0:
            try:
                response['error'].append("Username is already taken")
            except:
                response['error'] = []
                response['error'].append("Username is already taken")
        return response
    
    def addUser(self, postData):
        password = postData['password']
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        newuser = User.objects.create(first_name = postData['first_name'], last_name = postData['last_name'], email = postData['email'], username = postData['username'], date = postData['dob'], password = hashed_pw)
        return newuser

    def editUser(self, postData, user_id):
        update = User.objects.get(id = user_id)
        update.email = postData['email']
        update.first_name = postData['first_name']
        update.last_name = postData['last_name']
        update.admin = postData['admin']
        update.username = postData['username']
        update.save()
        return user_id

    def edituser_user(self, postData, user_id):
        update = User.objects.get(id = user_id)
        update.first_name = postData['first_name']
        update.last_name = postData['last_name']
        update.email = postData['email']
        update.username = postData['username']
        update.save()
        return user_id

    def validatePass(self, postData, user_id):
        response = {}
        if postData['password'] != postData['confirm_password']:
            try:
                response['error'].append("Password and Confirm Password must match")
            except:
                response['error'] = []
                response['error'].append("Password and Confirm Password must match")
        if not PASS_REGEX.match(postData['password']):
            try:
                response['error'].append("Passwords must be at least 8 characters, including 1 lowercase, 1 uppercase, 1 special character, and 1 number")
            except:
                response['error'] = []
                response['error'].append("Passwords must be at least 8 characters, including 1 lowercase and 1 number")
        return response

    def editPass(self, postData, user_id):
        password = postData['password']
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = User.objects.get(id=user_id)
        user.password = hashed_pw
        user.save()
        return

    def editDesc(self, postData, user_id):
        user = User.objects.get(id = user_id)
        user.description = postData['description']
        user.save()
        return

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    username = models.CharField(max_length = 90)
    date = models.DateField(max_length = 8, null=True)
    password = models.CharField(max_length = 355)
    admin = models.BooleanField(default = False)
    description = models.CharField(max_length = 255, null=True)
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def __str__(self):
        return "User Full Name: {} {}, Email: {}, Username: {}, Password: {}".format(self.first_name, self.last_name, self.email, self.username, self.password)

class MessageManager(models.Manager):
    def validateMessage(self, postData):
        response = {}
        if len(postData['content']) < 1:
            response['error'] = []
            response['error'].append("You don't have a message to post.")
        return response
    def addMessage(self, postData, created_by, addressed_to):
        newmessage = Message.objects.create(content = postData['content'], user = created_by, addressee = addressed_to)
        return newmessage

class Message(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name = 'messages')
    addressee = models.ForeignKey(User, related_name = 'messages_to')
    objects = MessageManager()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def __str__(self):
        return self.content

class CommentManager(models.Manager):
    def validateComment(self, postData):
        response = {}
        if len(postData['content']) < 1:
            response['error'] = []
            response['error'].append("You don't have a message to post.")
        return response
    def addComment(self, postData, created_by, message_id):
        newcomment = Comment.objects.create(content = postData['content'], user = created_by, message = message_id)
        return newcomment

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name = 'comments')
    message = models.ForeignKey(Message, related_name = 'comments')
    objects = CommentManager()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def __str__(self):
        return self.content