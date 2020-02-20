from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt
from datetime import datetime, timedelta, timezone

def home(request):
    return render(request, 'home.html')

def register_page(request):
    return render(request, 'register.html')

def sign_in_page(request):
    return render(request, 'signin.html')

def normal_dashboard(request):
    if 'userid' not in request.session:
        return redirect('/')
    context = {
        'users': User.objects.all(),
        'user': User.objects.get(id = request.session['userid'])
    }
    return render(request, 'dashboard.html', context)

def admin_dashboard(request):
    if 'userid' not in request.session:
        return redirect('/')
    this_user = User.objects.get(id= request.session['userid'])
    if this_user.user_level != 9:
        messages.error(request, "Insuficient privedges to view this page.")
        return redirect('/signin')
    context = {
        'users': User.objects.all(),
        'user': User.objects.get(id = request.session['userid'])
    }
    return render(request, 'admindashboard.html', context)

def register(request):
    errors = User.objects.basic_validation(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)
        return redirect('/signin')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(first_name = request.POST['first'], last_name = request.POST['last'], email = request.POST['email'], password = pw_hash)
        if new_user.id == 1:
            new_user.user_level = 9
            new_user.save()
        return redirect('/signin')

def login_check(request):
    user = User.objects.filter(email = request.POST['email'])
    if len(user) == 0:
        messages.error(request, "Username not in our records")
        return redirect('/signin')
    if user: 
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            this_user = User.objects.get(id=request.session['userid'])
            if this_user.user_level == 9:
                return redirect('/dashboard/admin')
            else:
                return redirect('/dashboard')
        else:
            messages.error(request, "Incorrect Password")
            return redirect('/signin')
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def edit_own_profile(request):
    context = {
        'user': User.objects.get(id = request.session['userid'])
    }
    return render(request, 'myprofile.html', context)
def which_dashboard(request):
    this_user = User.objects.get(id = request.session['userid'])
    if this_user.user_level == 9:
        return redirect('/dashboard/admin')
    else:
        return redirect('/dashboard')

def edit_a_profile(request, id):
    if 'userid' not in request.session:
        return redirect('/')
    this_user = User.objects.get(id= request.session['userid'])
    if this_user.user_level != 9:
        messages.error(request, "Insuficient privedges to view this page.")
        return redirect('/signin')
    context = {
        'user_profile': User.objects.get(id=id)
    }
    return render(request, 'edit_user_profile.html', context)

def show_a_profile(request, id):
    if 'userid' not in request.session:
        return redirect('/')
    this_user = User.objects.get(id=id)
    all_posts = Message.objects.filter(user = this_user)
    for posts in all_posts:
        time_since = datetime.now().replace(tzinfo=timezone.utc) - posts.created_at
        time_since = time_since.total_seconds() // 60
        if time_since < 60:
            posts.formatted_time = f"{int(time_since)} minutes ago"
        elif time_since < 1440:
            time_since = time_since // 60
            posts.formatted_time = f"{int(time_since)} hours ago"
        elif time_since < 10080:
            time_since = time_since // 1440
            posts.formatted_time = f"{int(time_since)} days ago"
        else:
            posts.formatted_time = posts.created_at
        posts.save()

    context = {
        'user': this_user,
    }

    return render(request, 'show_user_profile.html', context)

def create_new_user_page(request):
    this_user = User.objects.get(id= request.session['userid'])
    if this_user.user_level != 9:
        messages.error(request, "Insuficient privedges to view this page.")
        return redirect('/signin')
    return render(request, 'add_new_user.html')

def admin_create_user(request):
    
    errors = User.objects.basic_validation(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)
        return redirect('/dashboard/admin')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(first_name = request.POST['first'], last_name = request.POST['last'], email = request.POST['email'], password = pw_hash)
        if new_user.id == 1:
            new_user.user_level = 9
            new_user.save()
        return redirect('/dashboard/admin')

def delete_user(request, id):
    this_user = User.objects.get(id= request.session['userid'])
    if this_user.user_level != 9:
        messages.error(request, "Insuficient privedges to perform this action.")
        return redirect('/signin') 
    this_user = User.objects.get(id=id)
    this_user.delete()
    return redirect('/dashboard/admin')

def update_password(request, id):
    this_user = User.objects.get(id=id)
    errors = {}
    if len(request.POST['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."
    if request.POST['password'] != request.POST['confirm']:
            errors['confirm'] = "Password and confirmed password did not match."
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)
        return redirect('/')
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    this_user.password = pw_hash
    this_user.save()
    return redirect('/dashboardroute')

def add_new_post(request):
    this_user = User.objects.get(id = request.POST['pageowner'])
    post_creator = User.objects.get(id = request.session['userid'])
    Message.objects.create(note = request.POST['note'],user = this_user, created_by2 = post_creator)
    return redirect('/users/show/'+str(this_user.id))

def add_new_comment(request):
    this_user = User.objects.get(id = request.POST['pageowner'])
    post_creator = User.objects.get(id = request.session['userid'])
    this_message = Message.objects.get(id=request.POST['thismessage'])
    Comment.objects.create(comment = request.POST['commenttext'],user = this_user, created_by2 = post_creator, message = this_message)
    return redirect('/users/show/'+str(this_user.id))

def update_my_info(request):
    this_user = User.objects.get(id = request.session['userid'])
    this_user.email = request.POST['email']
    this_user.first_name = request.POST['firstname']
    this_user.last_name = request.POST['lastname']
    this_user.save()
    return redirect('/dashboardroute')

def update_my_description(request):
    this_user = User.objects.get(id = request.session['userid'])
    this_user.desc = request.POST['description']
    this_user.save()
    return redirect('/dashboardroute')

def edit_user_info(request, id):
    this_user = User.objects.get(id=id)
    this_user.email = request.POST['email']
    this_user.first_name = request.POST['firstname']
    this_user.last_name = request.POST['lastname']
    if request.POST['userlevel'] == "Admin":
        this_user.user_level = 9
    if request.POST['userlevel'] == "Normal":
        this_user.user_level = 0
    this_user.save()
    return redirect('/dashboardroute')