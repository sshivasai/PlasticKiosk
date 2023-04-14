from category.models import category
from .models import aboutus as a
def aboutus_links(request):
    aboutus = a.objects.first()
    return dict(aboutus=aboutus)
