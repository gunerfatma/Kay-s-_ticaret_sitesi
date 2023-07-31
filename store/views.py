
from django.shortcuts import render,get_object_or_404
from .models import Urunler
from Category.models import Category

def store(request,category_slug=None):
     categories = None
     urunler = None

     if category_slug !=None:
          categories = get_object_or_404(Category, slug=category_slug)
          urunler = Urunler.objects.filter(Category=categories, is_available=True)
          urun_count = urunler.count()

     else:
          urunler = Urunler.objects.all().filter(is_available=True)
          urun_count=urunler.count()


     context = {
            'urunler':urunler,
            'urunler_count':urun_count,
        }
     return render(request, 'store/store.html',context)

def urun_detail(request, category_slug,urun_slug):
     try:
          single_urun = Urunler.objects.get(category__slug=category_slug, slug=urun_slug)
     except Exception as e:
          raise e
     
     context = {
          'single_urun':single_urun,
     } 
     return render(request, 'store/urun_detail.html',context)