from category.models import category as c

def menu_links(request):
    categories = c.objects.all()
    return dict(categories=categories)

