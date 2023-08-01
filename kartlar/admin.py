from django.contrib import admin
from .models import Kart, KartItem

class KartAdmin(admin.ModelAdmin):
    list_play = ('kart_id', 'Tarih_ekle')

class KartItemAdmin(admin.ModelAdmin):
    list_play = ('urun', 'kart','Miktar', 'is_active')

admin.site.register(Kart, KartAdmin)
admin.site.register(KartItem, KartItemAdmin)

