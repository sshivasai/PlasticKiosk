
from .models import stores
def warehouses_links(request):
    warehouses = stores.objects.filter(storetype__name = "WareHouse")
    return dict(warehouses=warehouses)


def kiosks_links(request):
    kiosks = stores.objects.filter(storetype__name = "Kiosk")
    return dict(kiosks=kiosks)