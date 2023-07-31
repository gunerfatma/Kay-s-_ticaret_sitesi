from django.shortcuts import render
from store.models import Urunler

def home(request):
    urunler = Urunler.objects.all().filter(is_available=True)

    context = {
        'urunler':urunler
    }
    return render(request,'home.html',context)