from django.db import models
from Account.models import Accounts
from store.models import Urunler, Variation

class Kart(models.Model):
    kart_id = models.CharField(max_length=250, blank=True)
    Tarih_ekle = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.kart_id
    
class KartItem(models.Model):
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE, null=True)
    urun = models.ForeignKey(Urunler, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank= True)
    kart = models.ForeignKey(Kart, on_delete=models.CASCADE, null=True)
    Miktar = models.IntegerField()
    is_active = models.BooleanField(default=True)


    def sub_total(self):
        return self.urun.fiyat * self.Miktar
    
    
    def __unicode__(self):
        return self.urun
    
    
