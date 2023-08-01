from django.http import HttpResponse
from django.shortcuts import redirect, render,get_object_or_404

from kartlar.models import KartItem
from siparis.models import SiparisUrun
from .forms import PuanlamaForm
from .models import ProductGallery, Puanlama, Urunler
from Category.models import Category
from kartlar.views import _kart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.contrib import messages



def store(request,category_slug=None):
     categories = None
     urunler = None

     if category_slug !=None:
          categories = get_object_or_404(Category, slug=category_slug)
          urunler = Urunler.objects.filter(category=categories, is_available=True)
          paginator = Paginator(urunler, 1)
          page = request.GET.get('page')
          paged_products = paginator.get_page(page)
          urun_count = urunler.count()

     else:
          urunler = Urunler.objects.all().filter(is_available=True).order_by('id')
          paginator = Paginator(urunler, 3)
          page = request.GET.get('page')
          paged_products = paginator.get_page(page)
          urun_count = urunler.count()


     context = {
            'urunler':paged_products,
            'urun_count':urun_count,
        }
     return render(request, 'store/store.html',context)



def urun_detail(request, category_slug,urun_slug):
     try:
          single_urun = Urunler.objects.get(category__slug=category_slug, slug=urun_slug)
          in_kart = KartItem.objects.filter(kart__kart_id =_kart_id(request), urun=single_urun).exists()
     except Exception as e:
          raise e
     
     if request.user.is_authenticated:
        try:
            orderproduct = SiparisUrun.objects.filter(user=request.user, urun_id=single_urun.id).exists()
        except SiparisUrun.DoesNotExist:
            orderproduct = None
     else:
        orderproduct = None

  
     puanlamas = Puanlama.objects.filter(urun_id=single_urun.id, status=True)

   
     product_gallery = ProductGallery.objects.filter(urun_id=single_urun.id)
  

     context = {
        'single_urun': single_urun,
        'in_kart'       : in_kart,
        'orderproduct': orderproduct,
        'puanlamas': puanlamas,
        'product_gallery': product_gallery,
       
    }
     return render(request, 'store/urun_detail.html', context)



def search(request):
     if 'keyword' in request.GET:
          keyword = request.GET['keyword']
          if keyword:
               urunler = Urunler.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(urun_adi__icontains=keyword))
               urun_count = urunler.count()
          context = {
               'urunler': urunler,
               'urun_count':urun_count,
               
          }
          return render(request, 'store/store.html', context )


def sumbit_puan(request, urun_id):
     url = request.META.get('HTTP_REFERER')
     if request.method == 'POST':
        try:
            puanlamas = Puanlama.objects.get(user__id=request.user.id, urun__id=urun_id)
            form = PuanlamaForm(request.POST, instance=puanlamas)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except Puanlama.DoesNotExist:
            form = PuanlamaForm(request.POST)
            if form.is_valid():
                data = Puanlama()
                data.subject = form.cleaned_data['subject']
                data.degerlendirme = form.cleaned_data['degerlendirme']
                data.puanlama = form.cleaned_data['puanlama']
                data.ip = request.META.get('REMOTE_ADDR')
                data.urun_id = urun_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)

