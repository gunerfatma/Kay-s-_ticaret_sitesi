from django.db import models
from django.urls import reverse
from Account.models import Accounts
from Category.models import Category
from django.db.models import Avg, Count


class Urunler(models.Model):
    urun_adi = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=1000, blank=True)
    fiyat = models.IntegerField()
    images = models.ImageField(upload_to='photo/urunler')
    stok = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('urun_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.urun_adi
    
    def averagePuanlama(self):
        puanlamas = Puanlama.objects.filter(urun=self, status=True).aggregate(average=Avg('degerlendirme'))
        avg = 0
        if puanlamas['average'] is not None:
            avg = float(puanlamas['average'])
        return avg
    
    def countPuanlama(self):
        puanlamas = Puanlama.objects.filter(urun=self, status=True).aggregate(count=Count('id'))
        count = 0
        if puanlamas['count'] is not None:
            count = int(puanlamas['count'])
        return count

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category ='color', is_active = True)

    def sizes(self):
         return super(VariationManager, self).filter(variation_category ='color', is_active = True)


variaton_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)

class Variation(models.Model):
    urun = models.ForeignKey(Urunler, on_delete= models.CASCADE)
    variation_category = models.CharField(max_length=100, choices = variaton_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default = True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __srt__(self):
        return self.variation_value
    

class Puanlama(models.Model):
    urun = models.ForeignKey(Urunler, on_delete=models.CASCADE)
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    puanlama = models.TextField(max_length=500, blank=True)
    degerlendirme = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
    

class ProductGallery(models.Model):
    urun = models.ForeignKey(Urunler, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products', max_length=255)

    def __str__(self):
        return self.urun.urun_adi

    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'


