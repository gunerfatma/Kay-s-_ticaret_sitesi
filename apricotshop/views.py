from django.shortcuts import render
from store.models import Puanlama, Urunler

def home(request):
    urunler = Urunler.objects.all().filter(is_available=True).order_by('created_date')

     # Get the reviews
    puanlamas = None
    for urun in urunler:
        puanlamas = Puanlama.objects.filter(urun_id=urun.id, status=True)


    context = {
        'urunler':urunler,
        'puanlamas': puanlamas,
    }
    return render(request,'home.html',context)