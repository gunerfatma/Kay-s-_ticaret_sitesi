
from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from kartlar.models import KartItem
from .forms import SiparisForm
from .models import Payment, Siparis, SiparisUrun
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import datetime
from store.models import Urunler
import json


def odemeler(request):
    body = json.loads(request.body)
    siparis = Siparis.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

  
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = siparis.order_total,
        status = body['status'],
    )
    payment.save()

    siparis.payment = payment
    siparis.is_ordered = True
    siparis.save()

    kart_items = KartItem.objects.filter(user=request.user)

    for item in kart_items:
        orderproduct = SiparisUrun()
        orderproduct.order_id = siparis.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.urun_id = item.urun_id
        orderproduct.quantity = item.quantity
        orderproduct.urun_price = item.urun.fiyat
        orderproduct.ordered = True
        orderproduct.save()

        kart_item = KartItem.objects.get(id=item.id)
        urun_variation = kart_item.variations.all()
        orderproduct = SiparisUrun.objects.get(id=orderproduct.id)
        orderproduct.variations.set(urun_variation)
        orderproduct.save()

        
        urun = Urunler.objects.get(id=item.urun_id)
        urun.stock -= item.quantity
        urun.save()

    
    KartItem.objects.filter(user=request.user).delete()

   
    mail_subject = 'Thank you for your order!'
    message = render_to_string('siparis/siparis_recieved_email.html', {
        'user': request.user,
        'siparis': siparis,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

   
    data = {
        'order_number': siparis.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)


    

def place_order(request, total=0, quantity=0):
    current_user = request.user

    kart_items = KartItem.objects.filter(user=current_user)
    kart_sayac = kart_items.count()
    if kart_sayac <= 0:
        return redirect('store')
    
    grand_total = 0
    tax = 0
    for kart_item in kart_items:
        total += (kart_item.urun.fiyat * kart_item.Miktar)
        quantity += kart_item.Miktar
    tax = (2 * total)/100
    grand_total = total + tax
    
    if request.method == 'POST':
        form = SiparisForm(request.POST)
        if form.is_valid():
            print(form.errors)
            data = Siparis()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
    

            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") 
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            siparis = Siparis.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'siparis': siparis,
                'kart_items': kart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            
            return render(request, 'siparis/odemeler.html', context)             
        else:
           return render(request, 'siparis/odemeler.html') 
    else:
        return redirect('checkout')
    
def siparis_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        siparis = Siparis.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = SiparisUrun.objects.filter(order_id=siparis.id)

        subtotal = 0
        for i in ordered_products:
            subtotal += i.urun_price * i.quantity

        payment = Payment.objects.get(payment_id=transID)

        context = {
            'siparis': siparis,
            'ordered_products': ordered_products,
            'order_number': siparis.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal,
        }
        return render(request, 'siparis/siparis_complete.html', context)
    except (Payment.DoesNotExist, Siparis.DoesNotExist):
        return redirect('home')
       