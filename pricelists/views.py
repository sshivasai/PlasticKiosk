from django.shortcuts import render
from pricelists.models import pricelists as p
from category.models import category as c
# Create your views here.
def pricelists_details(request,name):
    category = c.objects.all().filter(name = name).first()
    try:
        temp = p.objects.all()
        prices = []
        for x in temp:
            if str(x.category) == name:
                prices.append(x)
    except Exception as e:
        raise e
    context = {
        'prices': prices,
        'category':category,
    }
    return render(request,'pricelists/pricelists_details.html',context)