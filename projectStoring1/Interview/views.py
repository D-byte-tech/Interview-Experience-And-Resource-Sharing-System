from email import message
from django.contrib import messages, auth
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as main_login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect,HttpResponse
from Interview.models import TestUser,InterviewDatabase,ResourceDatabase,Profile
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from .import forms
from django.db.models.functions import Lower
from .helper import send_forget_pwd_mail
import uuid

from .forms import UserUpdateForm, ProfileUpdateForm

# Create your views here.

def welcome(request):
    return render(request, 'welcome.html')


@login_required(login_url='login')
def index(request):

    current = request.user
    userid = current.id

    me = Profile.objects.get(user=userid)
    role = me.role

    dik=User.objects.get(id=userid)

    context = {'me':me, 'role':role, 'dik':dik}
    

    return render(request, 'index.html', context)


def userinfo(request):
    #return HttpResponse("this is userinfo")
    if request.method=="POST":
       first_name = request.POST['first_name']
       last_name = request.POST['last_name']
       email = request.POST['email']
       phone = request.POST['phone']

       test = TestUser(first_name=first_name, last_name=last_name, email=email, phone=phone)
       test.save()
    return render(request, 'Userinfo.html')

#def interview(request):
    #return HttpResponse("this is interview")
    #if request.method=="POST":
       # date = request.POST['date']
       # year = request.POST['year']
       # cname = request.POST['cname']
       # branch = request.POST['branch']
       # title = request.POST['title']
       # interexp = request.POST['interexp']
       # file = request.FILES['file']

       # fs=FileSystemStorage()
        
       # inter= InterviewDatabase(date=date, year=year, cname=cname, branch=branch, title=title, interexp=interexp, file=file)
       # inter.save()
    
    #return render(request, 'Interview.html')
       


#def resource(request):
    #return HttpResponse("this is resource")
    
    #if request.method=="POST":
        #date = request.POST['date']
        #sname = request.POST['sname']
        #topic = request.POST['topic']
        #resourceDesc = request.POST['resourceDesc']
        #file = request.FILES['file']

        #fs=FileSystemStorage()

        #res= ResourceDatabase(date=date, sname=sname, topic=topic, resourceDesc=resourceDesc, file=file)
        #res.save()

    #return render(request, 'Resource.html')

@login_required(login_url='login')
def interview(request):
    #return HttpResponse("this is interview")
    if request.method=="POST":
       form=forms.CreateInterviewDatabase(request.POST,request.FILES)
       if form.is_valid():
           instance= form.save(commit=False)
           instance.Userid=request.user
           instance.save()
           return redirect('/index')
    else:
           form=forms.CreateInterviewDatabase()
           return render(request,'Interview.html')
       
    return render(request, 'Interview.html')

@login_required(login_url='login')
def resource(request):
    #return HttpResponse("this is resource")
    if request.method=="POST":
       form=forms.CreateResourceDatabase(request.POST,request.FILES)
       if form.is_valid():
           instance= form.save(commit=False)
           instance.Userid=request.user
           instance.save()
           return redirect('/index')
    else:
           form=forms.CreateResourceDatabase()
           return render(request,'Resource.html')
       
    return render(request, 'Resource.html')


def signup(request):
    if request.method=="POST":
        # Get the post parameters
        role = request.POST['role']
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        branch = request.POST['branch']
        email = request.POST['email']
        uname = request.POST['uname']
        psw = request.POST['psw']
        cname = request.POST.get('companyName')
        yoj = request.POST.get('yoj')
        linkedIn = request.POST['linkedIn']
        print(role, fname, lname, branch, email, cname, yoj)

        if User.objects.filter(username = uname).first():
            messages.error(request, 'This username is already taken')
            return redirect('/signup')

        # Create the user
        myuser = User.objects.create(username=uname, email=email)
        myuser.set_password(psw)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.profile.role = role
        myuser.profile.branch = branch
        myuser.profile.company_name = cname
        myuser.profile.yoj = yoj
        myuser.profile.linkedIn = linkedIn
        myuser.save()
        
        #messages.success(request, 'Your account has been successfully created')
        return redirect('/login')
    return render(request, 'signup.html')


def user_login(request):
    if request.method == "POST":
        # Get the post parameters
        loginuname = request.POST['loginuname']
        loginpsw = request.POST['loginpsw']
        print("\nentered username-->", loginuname)
        print("entered password-->", loginpsw)

        user_object = User.objects.filter(username=loginuname).first()
        
        if user_object:
            """
            if you find user_object then you have to check the password(which was entered 
            by user) to the password which is stored in database.
            """
            if user_object.check_password(loginpsw):
                # password matched.
                main_login(request, user_object)
                #messages.success(request, "Successfully Logged In")
                return redirect('/index')
            else:
                # password is not correct.
                messages.error(request, "Invalid Password, Please try again!")
                return redirect('/login')
        else:
            # username entered by USER does not exist in the database
            messages.error(request, "User name Does not exist, Please try again!")
            return redirect('/login')

    else:
        return render(request, 'login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


@login_required(login_url='login')
def interviewtile(request):

    current = request.user
    userid = current.id

    wiki = InterviewDatabase.objects.all()
    biki = wiki.values('cname').distinct()
    dests = biki.order_by(Lower('cname'))

    dik=User.objects.get(id=userid)

    context = {'dests':dests, 'dik':dik}
    
    return render(request, 'interviewtile.html' , context)


@login_required(login_url='login')
def resourcetile(request):

    current = request.user
    userid = current.id

    wiki = ResourceDatabase.objects.all()
    biki = wiki.values('sname').distinct()
    dests = biki.order_by('sname')

    dik=User.objects.get(id=userid)

    context = {'dests':dests, 'dik':dik}

    return render(request, 'resourcetile.html' ,  context)


@login_required(login_url='login')
def interviewExperiences(request, cname ):

   current = request.user
   userid = current.id

   wlogs = InterviewDatabase.objects.filter(cname=cname)
   blogs = reversed(wlogs.order_by('year'))
   

   dik=User.objects.get(id=userid)

   context = {'blogs':blogs, 'dik':dik}

  
   return render(request, 'interviewExperiences.html', context)


@login_required(login_url='login')
def resources(request, sname ):

   current = request.user
   userid = current.id

   vlogs = ResourceDatabase.objects.filter(sname=sname)

   dik=User.objects.get(id=userid)

   context = {'vlogs':vlogs, 'dik':dik}
  
   return render(request, 'resources.html', context)


@login_required(login_url='login')
def profiletest(request, Userid):

    current = request.user
    my = current.username

    test=User.objects.get(username=Userid)
    id= test.id

    myy = test.username

    print(id)
    west = Profile.objects.get(user=id)
    print(test)
    print(west)
    
    context={
        'test':test,
        'west':west,
        'my' : my,
        'myy' : myy
    }
   
    print(context)

    return render(request, 'profiletest.html',context)


@login_required(login_url='login')
def updateProfile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('/profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'updateProfile.html', context)


@login_required(login_url='login')
def user_profile(request):
    
    # dictionary for initial data with
    # field names as keys

    current_user = request.user
    current_user_id=current_user.id
    email=current_user.email
    fname=current_user.first_name
    lname=current_user.last_name
    print(current_user_id)

    context ={}
 
    # add the dictionary during initialization
    profile_obj = Profile.objects.get(user = current_user_id)
    profile_dict = dict()
    profile_dict['user'] = profile_obj.user
    profile_dict['email'] = email
    profile_dict['fname'] = fname
    profile_dict['lname'] = lname
    profile_dict['role'] = profile_obj.role
    profile_dict['branch'] = profile_obj.branch
    profile_dict['cname'] = profile_obj.company_name
    profile_dict['yoj'] = profile_obj.yoj
    profile_dict['linkedIn'] = profile_obj.linkedIn
    profile_dict['is_active'] = profile_obj.is_active
    profile_dict['is_staff'] = profile_obj.is_staff

    context["data"] = profile_dict
         
    return render(request, "userProfile.html", context)


def change_pwd(request, token):
    context = {}
    profile_obj = Profile.objects.filter(forget_pwd_token = token).first()
    context = {'user_id' : profile_obj.user.id}

    if request.method == 'POST':
        new_pwd = request.POST.get('new_pwd')
        confirm_pwd = request.POST.get('confirm_pwd')
        user_id = request.POST.get('user_id')

        if user_id is None:
            messages.error(request, 'No user id found.')
            return redirect(f'/changepwd/{token}')
        if new_pwd != confirm_pwd:
            messages.error(request, 'Both should be same.')
            return redirect(f'/changepwd/{token}')

        user_obj = User.objects.get(id = user_id)
        user_obj.set_password(new_pwd)
        user_obj.save()
        print(user_obj.password)
        return redirect('/login')

    return render(request, 'changePwd.html', context)


def forget_pwd(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        if not User.objects.filter(username=username).first():
            messages.error(request, 'No user found with this username.')
            return redirect('/forgetpwd')

        user_obj = User.objects.get(username=username)
        token = str(uuid.uuid4())
        profile_obj = Profile.objects.get(user = user_obj)
        profile_obj.forget_pwd_token = token
        profile_obj.save()
        send_forget_pwd_mail(user_obj.email, token)
        messages.success(request, 'An email is sent.')
        return redirect('/forgetpwd')
    
    return render(request, 'forgetPwd.html')







