from django.shortcuts import render,HttpResponse
from django.db.models import Q
from .models import stores as s
from .models import storetypes
# Create your views here.
def search(request,keyword=None):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if str(keyword).lower() =='all' or "":
             stores = s.objects.all()
        else :
            stores = s.objects.all().filter(Q(address__icontains=keyword)| Q(name__icontains=keyword))
        store_count = stores.count()

    context = {
        'stores': stores,
        'store_count': store_count,
        'keyword':keyword
    }
    return render(request, 'stores/search.html', context)