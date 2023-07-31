from django.contrib import admin
from .models import Urunler

class UrunAdmin(admin.ModelAdmin):
    list_display = ('urun_adi', 'fiyat','stok','Category','modify_date','is_available')
    prepopulated_fields = {'slug':('urun_adi',)}

admin.site.register(Urunler,UrunAdmin)
    