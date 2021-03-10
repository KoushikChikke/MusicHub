from django.shortcuts import render
from musicbeats.models import Song, WatchLater, History
from django.db.models import Case, When
def index(request):
    song = Song.objects.all()[:5]
    wl=None
    hist=None
    ids=[]
    ids_history=[]
    if request.user.is_authenticated:
        wl = WatchLater.objects.filter(user=request.user)[:5]
        for i in wl:
            ids.append(i.video_id)
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
        wl = Song.objects.filter(song_id__in=ids).order_by(preserved)

    return render(request, 'musicbeats/index.html', {'song':song,'liked':wl})
