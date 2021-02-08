from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm,UploadFileForm
from django.contrib import messages
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from .models import ip,File,Comment
import datetime
import httpagentparser
from .decorators import unauthenticated_user,allowedUsers,admin_only
from django.contrib.auth.models import Group,User
from django.db.models import Count
from .tasks import schedulerDelete
from django.utils import timezone

@unauthenticated_user
def register(request):
    
    form=CreateUserForm()
    if request.method=="POST":
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get('username')
            group=Group.objects.get(name='customer')
            user.groups.add(group)
            messages.success(request,f"Account created {username}")
            return redirect('login')
    context={'form':form,'title':'Register'}
    return render(request,'account/register.html',context)


@unauthenticated_user
def login(request):
    context={'title':"Login"}
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user:
            auth_login(request,user)
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            agent = request.META["HTTP_USER_AGENT"]
            s = httpagentparser.detect(agent)["os"]
            if x_forwarded_for:
                ipaddress = x_forwarded_for.split(',')[-1].strip()
            else:
                ipaddress = request.META.get('REMOTE_ADDR')
            get_ip= ip() 
            get_ip.ip_address= ipaddress
            get_ip.pub_date = datetime.date.today()
            get_ip.username=username
            get_ip.os=s
            get_ip.save()
            return redirect('home')
        else:
            messages.info(request,'username or password is not correct')
            return redirect('login')
    return render(request,'account/login.html',context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    context={'title':"Home"}
    return render(request,'account/home.html',context)

@login_required(login_url='login')
@allowedUsers(allowed_roles=['customer'])
def userPage(request):
    context={'title':'User Page'}
    return render(request,'account/user.html')

@login_required(login_url='login')
@admin_only
def adminPage(request):
    ipTable=ip.objects.all()
    context={
        'items':ipTable,
        'title':'Admin Ip Table'
    }
    return render(request,'account/adminPage.html',context)

@login_required(login_url='login')
@allowedUsers(allowed_roles=['customer'])
def sharefile(request):
    users=User.objects.all()
    if request.method=="POST" and request.FILES.get('file'):
        title=request.POST.get('title')
        content=request.POST.get('content')
        file=request.FILES.get('file')
        dateposted=datetime.date.today()
        showPermit=request.POST.getlist('show')
        commentPermit=request.POST.getlist('comment')
        fileinstance=File.objects.create(username_id=request.user.id,title=title,content=content,file=file,date_posted=dateposted)
        for i in showPermit:
            fileinstance.showPermit.add(i)
        for i in commentPermit:    
            if i in  showPermit:
                fileinstance.commentPermit.add(i)
        return redirect('user')
    context={'title':'Share Page','users':users}
    return render(request,'account/sharefile.html',context)


@login_required(login_url='login')
@allowedUsers(allowed_roles=['customer'])
def yourfiles(request):
    files=File.objects.filter(username_id=request.user.id)
    schedulerDelete()
    context={'title':'Your files','files':files}
    return render(request,'account/yourfiles.html',context)


@login_required(login_url='login')
@allowedUsers(allowed_roles=['customer'])
def deletefile(request,file_id):
    instance = get_object_or_404(File,id=file_id)
    instance.delete()
    return redirect('yourfiles')

@login_required(login_url='login')
@allowedUsers(allowed_roles=['customer'])
def edit(request,file_id):
    
    instance = get_object_or_404(File,id=file_id)
    users=User.objects.all()
    showed=instance.showPermit.all
    commented=instance.commentPermit.all
    if request.method=="POST" :
        instance.title=request.POST.get('title')
        instance.content=request.POST.get('content')
        instance.date_updated=datetime.date.today()
        if request.FILES.get('file') is not None:
            instance.file=request.FILES.get('file')
        showPermit=request.POST.getlist('show')
        commentPermit=request.POST.getlist('comment')
        
        # post=File(username_id=request.user.id,title=title,content=content,file=file,showPermit=showPermit,commentPermit=commentPermit)
        for i in showPermit:
            instance.showPermit.set(i)
        for i in commentPermit:    
            if i in  showPermit:
                instance.commentPermit.set(i)
        instance.save()
        return redirect('yourfiles')
       

    context={"title":"Edit File",'users':users,'instance':instance,'showed':showed,'commented':commented}
    return render(request,'account/editfile.html',context)


@login_required(login_url='login')
@allowedUsers(allowed_roles=['customer'])
def sharedfiles(request):
    fileShow=File.objects.filter(showPermit=request.user.id)
    fileComment=File.objects.filter(commentPermit=request.user.id)
    myfiles=File.objects.filter(username_id=request.user.id)
    context={'title':'Shared files','fileShow':fileShow,'fileComment':fileComment,'myfiles':myfiles}
    return render(request,'account/sharedfiles.html',context)


@login_required(login_url='login')
@allowedUsers(allowed_roles=['customer'])
def file(request,file_id):
    instance = get_object_or_404(File,id=file_id)
    comments=Comment.objects.all()
    showed=instance.showPermit.all
    commented=instance.commentPermit.all
    if request.method=="POST" :
        content=request.POST.get('comment')
        dateComment=datetime.date.today()
        Comment.objects.create(user=request.user,content=content,post=instance,date_comment=dateComment)
        return redirect('file',instance.id)
    context={'title':'File','instance':instance,'showed':showed,'commented':commented,'comments':comments}
    return render(request,'account/file.html',context)



@login_required(login_url='login')
@allowedUsers(allowed_roles=['customer'])
def deletecomment(request,file_id,comment_id):
    instance = get_object_or_404(Comment,id=comment_id)
    filee = get_object_or_404(File,id=file_id)
    if filee.username==request.user:
        instance.delete()
    elif instance.user==request.user:
        instance.delete()    
    return redirect('file',filee.id)



@login_required(login_url='login')
@allowedUsers(allowed_roles=['customer'])
def editcomment(request,file_id,comment_id):
    comment=get_object_or_404(Comment,id=comment_id)
    filee=get_object_or_404(File,id=file_id)
    if request.method=="POST":
        comment.content=request.POST.get('comment')
        comment.date_edited=datetime.date.today()
        comment.save()
        return redirect('file',filee.id)
    context={'title':'Edit Comment','comment':comment,'filee':filee}
    return render(request,"account/editcomment.html",context)