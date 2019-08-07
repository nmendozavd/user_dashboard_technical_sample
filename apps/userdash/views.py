from __future__ import unicode_literals

from .models import *
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages

def index(request):
    return render(request, 'userdash/index.html')

def register(request):
    return render(request, 'userdash/register.html')

def adminregister(request):
    try:
        id = request.session['id']
    except:
        return redirect('/dashboard')
    the_user = User.objects.get(id = request.session['id'])
    if not the_user.admin:
        return redirect('/dashboard')
    else:
        return render(request, 'userdash/addnew.html')

def login(request):
    return render(request, 'userdash/login.html')

def processadd(request):
    if request.method == 'POST':
        check_submission = User.objects.validateRegistration(request.POST)
        if len(check_submission) > 0:
            for message in check_submission['error']:
                messages.error(request, message)
            return redirect('/register')
        else:
            newuser = User.objects.addUser(request.POST)
            request.session['id'] = newuser.id
            if newuser.id == 1:
                newuser.admin = True
                newuser.save()
            return redirect('/dashboard')
    else:
        print 'get out of add'
        return redirect('/dashboard')

def processaddadmin(request):
    if request.method == 'POST':
        the_user = User.objects.get(id = request.session['id'])
        if not the_user.admin:
            return redirect('/dashboard')
        else:
            check_submission = User.objects.validateRegistration(request.POST)
            if len(check_submission) > 0:
                for message in check_submission['error']:
                    messages.error(request, message)
                return redirect('/users/addnew')
            else:
                newuser = User.objects.addUser(request.POST)
                messages.success(request, 'You have successfully added new user ' + str(newuser.first_name))
                print newuser
                print request.session['id']
                return redirect('/users/addnew')
    else:
        print 'get out of add'
        return redirect('/dashboard')

def processlogin(request):
    if request.method == 'POST':
        if len(request.POST['user_input']) < 1 or len(request.POST['password']) < 8:
            messages.warning(request, 'Invalid login information')
            return redirect('/signin')
        user = User.objects.validateLogin(request.POST)
        if user:
            request.session['id'] = user
            return redirect('/dashboard')
        else:
            messages.warning(request, 'Invalid login information')
            return redirect('/signin')
        return redirect('/')
    else:
        print 'get out of login'
        return redirect('/')

def logout(request):
    try:
        del request.session['id']
        return redirect('/')
    except:
        return redirect('/')

def home(request):
    try:
        request.session['id']
        print 'logged in'
    except:
        return redirect('/signin')
    checkuser = User.objects.get(id = request.session['id'])
    if not checkuser.admin:
        context = {
            'user':User.objects.get(id = request.session['id']),
            'all_users': User.objects.exclude(id = request.session['id']),
        }
        return render(request, 'userdash/user_home.html', context)
    elif checkuser.admin:
        return redirect('/dashboard/admin')

def adminhome(request):
    try:
        request.session['id']
    except:
        return redirect('/login')
    checkuser = User.objects.get(id = request.session['id'])
    if not checkuser.admin:
        return redirect('/dashboard')
    elif checkuser.admin:
        context = {
            'user':User.objects.get(id = request.session['id']),
            'all_users': User.objects.exclude(id = request.session['id']).order_by('first_name'),
        }
        return render(request, 'userdash/admin_home.html', context)

def adminedit(request, user_id):
    try:
        request.session['id']
    except:
        return redirect('/login')
    checkuser = User.objects.get(id = request.session['id'])
    if not checkuser.admin:
        return redirect('/edit')
    elif checkuser.admin:
        context = {
            'user':User.objects.get(id = user_id),
        }
        return render(request, 'userdash/admin_edit.html', context)

def edit_user(request, user_id):
    if request.method == 'POST':
        the_user = User.objects.get(id = user_id)
        if not the_user.admin:
            return redirect('/edit')
        else:
            check_submission = User.objects.validateEdit(request.POST, user_id)
            if len(check_submission) > 0:
                for message in check_submission['error']:
                    print message
                    messages.error(request, message)
                    print messages.error
                return redirect('/users/edit/'+str(user_id))
            else:
                update = User.objects.editUser(request.POST, user_id)
                messages.success(request, 'Successfully updated user info')
                return redirect('/users/edit/'+str(user_id))
    else:
        print 'get out of edit_user'
        return redirect('/')

def edit_pass(request, user_id):
    if request.method == 'POST':
        the_user = User.objects.get(id = request.session['id'])
        if not the_user.admin:
            if int(the_user.id) == int(user_id):
                check_submission = User.objects.validatePass(request.POST, user_id)
                if len(check_submission) > 0:
                    for message in check_submission['error']:
                        print message
                        messages.error(request, message)
                        print messages.error
                else:
                    update = User.objects.editPass(request.POST, user_id)
                    messages.success(request, 'Successfully updated user info')
                    return redirect('/users/edit')
            else:
                return redirect('/dashboard')
        else:
            check_submission = User.objects.validatePass(request.POST, user_id)
            if len(check_submission) > 0:
                for message in check_submission['error']:
                    messages.error(request, message)
            else:
                update = User.objects.editPass(request.POST, user_id)
                messages.success(request, 'Successfully updated user info')
                return redirect('/users/edit/'+str(user_id))
    else:
        print 'get out of edit_pass'
        return redirect('/users/edit/'+str(user_id))

def show(request, user_id):
    context = {
            'user':User.objects.get(id = user_id),
            'user_messages': Message.objects.filter(addressee = user_id),
        }
    return render(request, 'userdash/show.html', context)

def addmessage(request, user_id):
    if request.method == 'POST':
        try:
            creator = User.objects.get(id = request.session['id'])
            addressee = User.objects.get(id = user_id)
        except:
            return redirect('/users/show/'+str(user_id))
        check_submission = Message.objects.validateMessage(request.POST)
        if len(check_submission) > 0:
            messages.error(request, check_submission['error'])
            return redirect('/users/show/'+str(user_id))
        else:
            new_message = Message.objects.addMessage(request.POST, creator, addressee)
            return redirect('/users/show/'+str(user_id))
    else:
        print 'get out of addmessage'
        return redirect('/users/show/'+str(user_id))

def addcomment(request, user_id, message_id):
    if request.method == 'POST':
        try:
            creator = User.objects.get(id = request.session['id'])
            addressee = User.objects.get(id = user_id)
        except:
            return redirect('/users/show/'+str(user_id))
        check_submission = Comment.objects.validateComment(request.POST)
        if len(check_submission) > 0:
            messages.error(request, check_submission['error'])
            return redirect('/users/show/'+str(user_id))
        else:
            message = Message.objects.get(id = message_id)
            user = User.objects.get(id = request.session['id'])
            new_comment = Comment.objects.addComment(request.POST, user, message)
            return redirect('/users/show/'+str(user_id))
    else:
        print 'get out of addmessage'
        return redirect('/users/show/'+str(user_id))

def remove(request, user_id):
    try:
        request.session['id']
    except:
        return redirect('/login')
    checkuser = User.objects.get(id = request.session['id'])
    if not checkuser.admin:
        return redirect('/edit')
    return HttpResponse('learn to cascade first')

def edit_by_user(request):
    context = {
        'user':User.objects.get(id = request.session['id']),
    }
    return render(request, 'userdash/user_edit.html', context)

def user_update(request, user_id):
    if request.method == 'POST':
        if int(user_id) == int(request.session['id']):
            the_user = User.objects.get(id = request.session['id'])
            check_submission = User.objects.validateEdit(request.POST, user_id)
            if len(check_submission) > 0:
                for message in check_submission['error']:
                    print message
                    messages.error(request, message)
                    print messages.error
                return redirect('/users/edit')
            else:
                update = User.objects.edituser_user(request.POST, user_id)
                messages.success(request, 'Successfully updated your info')
                return redirect('/users/edit')
        else:
            print 'user cannot edit other pages'
            return redirect('/users/edit')
    else:
        print 'get out of user_update'
        return redirect('/')

def editdesc(request, user_id):
    if request.method == 'POST':
        if int(user_id) == int(request.session['id']):
            if len(request.POST['description']) < 1:
                message.error(request, 'Please enter a description')
                return redirect('/users/edit')
            the_user = User.objects.get(id = request.session['id'])
            update = User.objects.editDesc(request.POST, user_id)
            messages.success(request, 'Successfully updated your info')
            return redirect('/users/edit')
        else:
            print 'user cannot edit other pages'
            return redirect('/users/edit')
    else:
        print 'get out of edit desc'
        return redirect('/')