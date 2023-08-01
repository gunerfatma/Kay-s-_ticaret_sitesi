from django.shortcuts import get_object_or_404, redirect, render
from store.models import Urunler, Variation
from kartlar.models import Kart, KartItem
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse 
from django.contrib.auth.decorators import login_required


def _kart_id(request):
    kart = request.session.session_key
    if not kart:
        kart = request.session.create()
    return kart



def add_kart(request, urun_id):
    current_user = request.user
    urun = Urunler.objects.get(id=urun_id) 
  
    if current_user.is_authenticated:
        urun_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(urun=urun, variation_category__iexact=key, variation_value__iexact=value)
                    urun_variation.append(variation)
                except:
                    pass


        is_kart_item_exists = KartItem.objects.filter(urun=urun, user=current_user).exists()
        if is_kart_item_exists:
            kart_item = KartItem.objects.filter(urun=urun, user=current_user)
            ex_var_list = []
            id = []
            for item in kart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if urun_variation in ex_var_list:
               
                index = ex_var_list.index(urun_variation)
                item_id = id[index]
                item = KartItem.objects.get(urun=urun, id=item_id)
                item.Miktar += 1
                item.save()

            else:
                item = KartItem.objects.create(urun=urun, quantity=1, user=current_user)
                if len(urun_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*urun_variation)
                item.save()
        else:
            kart_item = KartItem.objects.create(
                urun = urun,
                Miktar = 1,
                user = current_user,
            )
            if len(urun_variation) > 0:
                kart_item.variations.clear()
                kart_item.variations.add(*urun_variation)
            kart_item.save()
        return redirect('kart')

    else:
        urun_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(urun=urun, variation_category__iexact=key, variation_value__iexact=value)
                    urun_variation.append(variation)
                except:
                    pass


        try:
            kart = Kart.objects.get(kart_id=_kart_id(request)) 
        except Kart.DoesNotExist:
            kart = Kart.objects.create(
                kart_id = _kart_id(request)
            )
        kart.save()

        is_kart_item_exists = KartItem.objects.filter(urun=urun, kart=kart).exists()
        if is_kart_item_exists:
            kart_item = KartItem.objects.filter(urun=urun, kart=kart)
           
            ex_var_list = []
            id = []
            for item in kart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            print(ex_var_list)

            if urun_variation in ex_var_list:
               
                index = ex_var_list.index(urun_variation)
                item_id = id[index]
                item = KartItem.objects.get(urun=urun, id=item_id)
                item.Miktar += 1
                item.save()

            else:
                item = KartItem.objects.create(urun=urun, quantity=1, kart=kart)
                if len(urun_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*urun_variation)
                item.save()
        else:
            kart_item = KartItem.objects.create(
                urun = urun,
                Miktar = 1,
                kart = kart,
            )
            if len(urun_variation) > 0:
                kart_item.variations.clear()
                kart_item.variations.add(*urun_variation)
            kart_item.save()
        return redirect('kart')


def remove_kart(request, urun_id, kart_item_id):
    urun = get_object_or_404(Urunler, id= urun_id)
    try:
        if request.user.is_authenticated:
            kart_item = KartItem.objects.get(urun= urun,  user=request.user, id=kart_item_id)
        else:
            kart = Kart.objects.get(kart_id=_kart_id(request))
            kart_item = KartItem.objects.get(urun=urun, kart=kart, id=kart_item_id)

        if kart_item.Miktar > 1:
            kart_item.Miktar -=1
            kart_item.save()
        else:
            kart_item.delete()
    except:
        pass
    return redirect('kart')

def remove_kart_item(request, urun_id, kart_item_id):
    urun = get_object_or_404(Urunler, id= urun_id)
    if request.user.is_authenticated:
        kart_item = KartItem.objects.get(urun=urun, user=request.user, id=kart_item_id)
    else:
        kart = Kart.objects.get(kart_id=_kart_id(request))
        kart_item = KartItem.objects.get(urun=urun, kart=kart, id=kart_item_id)
    kart_item.delete()
    return redirect('kart')




def kart(request, total = 0, quantity = 0, kart_items= None):
    try:
        vergi = 0
        grand_total = 0
        if request.user.is_authenticated:
            kart_items = KartItem.objects.filter(user=request.user, is_active=True)
        else:
            kart = Kart.objects.get(kart_id=_kart_id(request))
            kart_items=KartItem.objects.filter(kart=kart, is_active=True)
        for kart_item in kart_items:
            total+=(kart_item.urun.fiyat * kart_item.Miktar)
            quantity +=kart_item.Miktar
        vergi = (2* total)/100
        grand_total = total + vergi
    except ObjectDoesNotExist:
        pass

    context ={
        'total':total,
        'quantity': quantity,
        'kart_items':kart_items,
        'vergi'     : vergi,
        'grand_total':grand_total,
    }
    return render(request,'store/kart.html', context)

@login_required(login_url='login')
def checkout(request,  total = 0, quantity = 0, kart_items= None):
    try:
        vergi = 0
        grand_total = 0
        if request.user.is_authenticated:
             kart_items = KartItem.objects.filter(user=request.user, is_active=True)
        else:
            kart = Kart.objects.get(kart_id=_kart_id(request))
            kart_items=KartItem.objects.filter(kart=kart, is_active=True)
        for kart_item in kart_items:
            total+=(kart_item.urun.fiyat * kart_item.Miktar)
            quantity +=kart_item.Miktar
        vergi = (2* total)/100
        grand_total = total + vergi
    except ObjectDoesNotExist:
        pass

    context ={
        'total':total,
        'quantity': quantity,
        'kart_items':kart_items,
        'vergi'     : vergi,
        'grand_total':grand_total,
    }
    return render(request, 'store/checkout.html', context)