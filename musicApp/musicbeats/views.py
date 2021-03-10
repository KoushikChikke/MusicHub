from django.shortcuts import render
from musicbeats.models import Song, WatchLater, History, Channel, userExtended
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, HttpResponseRedirect,get_object_or_404
from django.db.models import Case, When
from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib import messages
import PIL 
from PIL import Image 

def index(request):
    song = Song.objects.all()
    print(song)
    return render(request, 'musicbeats/index.html', {'song':song})
def songs(request):
    song = Song.objects.all()
    paginator = Paginator(song, 4)
    page_number = request.GET.get('page')
    song = paginator.get_page(page_number)
    return render(request,'musicbeats/songs.html',{'song':song})
def songpost(request,id):
    song = Song.objects.filter(song_id=id).first()
    return render(request,'musicbeats/songpost.html',{'song':song})
def login(request):
    if request.method=="POST":
        username = request.POST['username']
        password =  request.POST['pass1']
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request,"Invalid Credentials!")
            return redirect('/musicbeats/login')
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
        profileImage =  request.FILES['profileImage']
        img = PIL.Image.open(profileImage) 
        wid, hgt = img.size 
        if User.objects.filter(username=username).exists():
            messages.error(request,"Username is taken, Please try another one!")
            return redirect('/musicbeats/signup')

        if len(username) > 15:
            messages.error(request,"Username must be less than 15 characters.")
            return redirect('/musicbeats/signup')
        
        if not username.isalnum():
            messages.error(request,"Username should only contain letters and numbers")
            return redirect('/musicbeats/signup')

        if pass1 != pass2:
            messages.error(request,"Password Does not match!. Please signup again.")
            return redirect('/musicbeats/signup')

        if (wid!=256 and hgt!=256):
            messages.error(request,"Please upload an image of resolution 256*256")
            return redirect('/musicbeats/signup')

        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = first_name
        myuser.last_name = last_name
        myuser.save()
        user = authenticate(username=username, password=pass1)
        from django.contrib.auth import login
        login(request, user)
        channel= Channel(name=username)
        #get object of specific user 
        from musicbeats.models import  userExtended
        userCustom= userExtended(user=request.user, picture=profileImage)
        userCustom.save()
        channel.save()
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
    paginator = Paginator(song, 5)
    page_number = request.GET.get('page')
    song = paginator.get_page(page_number)
    return render(request, 'musicbeats/watchlater.html',{'song':song})


def wl_delete(request,id):
    obj = WatchLater.objects.get(video_id = id,user=request.user)
    obj.delete() 
    return redirect('watchlater')

def search(request):
    query = request.GET.get("query")
    song = Song.objects.all()
    qs = song.filter(name__icontains=query)
    paginator = Paginator(qs, 2)
    page_number = request.GET.get('page')
    song = paginator.get_page(page_number)
    return render(request, 'musicbeats/search.html',{"songs":song,"query":query})
def songType(request,id):
    if id == 1:
        song = Song.objects.filter(tags="rock")
    elif(id == 2):
        song = Song.objects.filter(tags="jazz")
    elif(id == 3):
        song = Song.objects.filter(tags="pop")
    elif(id == 4):
        song = Song.objects.filter(tags="country")
    elif(id == 5):
        song = Song.objects.filter(tags="classical")
    elif(id == 6):
        song = Song.objects.filter(tags="heavyMetal")
    elif(id == 7):
        song = Song.objects.filter(tags="rap")
        
    paginator = Paginator(song, 5)
    page_number = request.GET.get('page')
    song = paginator.get_page(page_number)
    return render(request,'musicbeats/songs.html',{'song':song})


def history(request):
    if request.method=="POST":
        user = request.user
        music_id =  request.POST['music_id']
        history = History(user=user, music_id=music_id)
        print(music_id)
        print("im in")
        history.save()
        return redirect(f"/musicbeats/song/{music_id}")
    history = History.objects.filter(user=request.user)[:30]
    ids=[]
    for i in history:
        ids.append(i.music_id)
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    song = Song.objects.filter(song_id__in=ids).order_by(preserved)
    paginator = Paginator(song, 5)
    page_number = request.GET.get('page')
    history = paginator.get_page(page_number)
    return render(request,'musicbeats/history.html',{'history':history})

def channel(request, channel):
    chan = Channel.objects.filter(name=channel).first()
    song = None
    if chan!= None:
        video_ids = str(chan.music).split(" ")[1:]
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(video_ids)])
        song = Song.objects.filter(song_id__in=video_ids).order_by(preserved)
    return render(request,'musicbeats/channel.html',{'channel':chan,'song':song})

def upload(request):
    if request.method == "POST":
        name = request.POST['name']
        singer = request.POST['singer_name']
        tags =  request.POST['genre']
        image =  request.FILES['MusicImage']
        movie =  request.POST['movie_name']
        credit =  request.POST['credit']
        song =  request.FILES['Musicfile']
        description =  request.FILES['description']
        
        # fetching the dimensions 
        img = PIL.Image.open(image) 
        wid, hgt = img.size 
        # convert image object to sring
        sg = str(song)
        
        if not sg.endswith('.mp3'):
            messages.error(request,"only mp3 files are supported!")
            return redirect('/musicbeats/upload')
        if (wid!=256 and hgt!=256):
            messages.error(request,"Please upload an image of resolution 256*256")
            return redirect('/musicbeats/upload')
        song_model=Song(name=name,singer=singer,tags=tags,image=image,movie=movie,credit=credit,song=song,description=description)
        song_model.save()

        

        music_id = song_model.song_id
        channel_find = Channel.objects.filter(name=str(request.user))
        for i in channel_find:
            i.music += f" {music_id}"
            i.save()
            
    chan = Channel.objects.filter(name=channel).first()
    return render(request,'musicbeats/upload.html')
def browseChannels(request):
    
    return render(request, 'musicbeats/browseChannels.html')