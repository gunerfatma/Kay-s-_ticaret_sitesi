from django.db import models
from django.urls import reverse
from Category.models import Category


class Urunler(models.Model):
    urun_adi = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=200, blank=True)
    fiyat = models.IntegerField()
    images = models.ImageField(upload_to='photo/urunler')
    stok = models.IntegerField()
    is_available = models.BooleanField(default=True)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('urun_detail', args=[self.Category.slug, self.slug])

    def __str__(self):
        return self.urun_adi

