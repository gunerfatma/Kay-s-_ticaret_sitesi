from django.contrib import admin
from .models import Urunler,Variation,Puanlama,ProductGallery
import admin_thumbnails

@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

class UrunAdmin(admin.ModelAdmin):
    list_display = ('urun_adi', 'fiyat','stok','category','modify_date','is_available')
    prepopulated_fields = {'slug':('urun_adi',)}
    inlines = [ProductGalleryInline]

class VariationAdmin(admin.ModelAdmin):
    list_display = ('urun', 'variation_category','variation_value','is_active')
    list_editable =('is_active',)
    list_filter = ('urun', 'variation_category','variation_value' )

admin.site.register(Urunler,UrunAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(Puanlama)
admin.site.register(ProductGallery)
    