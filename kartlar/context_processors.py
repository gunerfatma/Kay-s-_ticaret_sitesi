from .models import Kart, KartItem
from .views import _kart_id

def sayac(request):
    kart_sayac=0
    if 'admin' in request.path:
        return {}
    else:
        try:
            kart =Kart.objects.filter(kart_id=_kart_id(request))
            if request.user.is_authenticated:
                kart_items = KartItem.objects.all().filter(user=request.user)
            else:
                kart_items = KartItem.objects.all().filter(kart=kart[:1])
            for kart_item in kart_items:
                kart_sayac += kart_item.Miktar
        except Kart.DoesNotExist:
            kart_sayac =0
    return dict(kart_sayac=kart_sayac)
