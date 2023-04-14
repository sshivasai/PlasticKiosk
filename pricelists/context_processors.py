from category.models import category
from .models import pricelists
def menu_links(request):
    temp = pricelists.objects.all()
    links  = []
    for x in temp :
        links.append(x.category)
    links = set(links)
    return dict(links=links)
