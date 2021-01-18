from django.shortcuts import render
from musicbeats.models import Song, WatchLater
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, HttpResponseRedirect
from django.db.models import Case, When
def index(request):
    song = Song.objects.all()
    return render(request, 'musicbeats/index.html', {'song':song})
def songs(request):
    song = Song.objects.all()
    return render(request,'musicbeats/songs.html',{'song':song})
def songpost(request,id):
    song = Song.objects.filter(song_id=id).first()
    return render(request,'musicbeats/songpost.html',{'song':song})
def login(request):
    if request.method=="POST":
        username = request.POST['username']
        password =  request.POST['pass1']
        user = authenticate(username=username, password=password)
        from django.contrib.auth import login
        login(request, user)
        return redirect('/')
    return render(request,'musicbeats/login.html')
def logout_user(request):
    # Loging out the user
    logout(request)
    return redirect('/')


def signup(request):
    if request.method=="POST":
        email = request.POST['email']
        username = request.POST['username']
        first_name =  request.POST['firstname']
        last_name =  request.POST['lastname']
        pass1 =  request.POST['pass1']
        pass2 =  request.POST['pass2']

        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = first_name
        myuser.last_name = last_name
        myuser.save()
        user = authenticate(username=username, password=pass1)
        from django.contrib.auth import login
        login(request, user)
        return redirect('/')
    return render(request,'musicbeats/signup.html')

def watchlater(request):
    if request.method=="POST":
        user = request.user
        video_id =  request.POST['video_id']
        watch = WatchLater.objects.filter(user=user)
        for i in watch:
            if video_id == i.video_id:
                message = "Your Video is already Added"
                break
               
        else:
            watchlater = WatchLater(user=user, video_id=video_id)
            watchlater.save()
            message = " Your video is Successfully Added"
            print(message)
        song = Song.objects.filter(song_id=video_id).first()
        return render(request,'musicbeats/songpost.html',{'song':song, 'message':message})
        # return redirect(f"/musicbeats/songs/{video_id}",  {'hello':'hello'})
    wl = WatchLater.objects.filter(user=request.user)
    ids=[]
    for i in wl:
        ids.append(i.video_id)
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    song = Song.objects.filter(song_id__in=ids).order_by(preserved)
    return render(request, 'musicbeats/watchlater.html',{'song':song})


def wl_delete(request,id):
    obj = WatchLater.objects.get(video_id = id,user=request.user)
    obj.delete() 
    return redirect('watchlater')

def search(request):
    query = request.GET.get("query")
    song = Song.objects.all()
    qs = song.filter(name__icontains=query)
    return render(request, 'musicbeats/search.html',{"songs":qs,"query":query})