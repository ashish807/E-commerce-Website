from django.contrib import admin
from django.db import models
from .models import Product, Variation, ReviewRating, ProductGallery, Appointments, BloodCategory, ProductDetailedDescriptionPanelCheck, Hospital
import admin_thumbnails
# Register your models here.


@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model =ProductGallery
    extra =1

class ProductAdmin(admin.ModelAdmin):
    list_display=('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [ProductGalleryInline]

admin.site.register(Product, ProductAdmin)


class VariationAdmin(admin.ModelAdmin):
    list_display=( 'product' ,'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value',)

class AppointmentsAdmin(admin.ModelAdmin):

    list_display = ['appointment_number', 'full_name', 'phone',  'is_billed','appointment_request_date', 'date', 'vendorConfirmation','bloodCollected','bloodAnalysed', 'reportUploaded']
    
    list_editable =['vendorConfirmation','bloodCollected','bloodAnalysed', 'reportUploaded']
    
    list_filter=['vendorConfirmation','bloodCollected','bloodAnalysed', 'reportUploaded']
    
    search_fields =['appointment_number', 'first_name', 'phone', 'email']
    
    list_per_page  =20

    list_editable = ['vendorConfirmation','bloodCollected','bloodAnalysed', 'reportUploaded']

class BloodCategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'category_price']

admin.site.register(Appointments, AppointmentsAdmin)

admin.site.register(Variation, VariationAdmin)

class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'subject', 'review','created_at', 'updated_at')

admin.site.register(ReviewRating, ReviewRatingAdmin)

admin.site.register(ProductGallery)

admin.site.register(BloodCategory, BloodCategoryAdmin)


class ProductDetailedDescriptionPanelCheckAdmin(admin.ModelAdmin):
    list_display=('product', 'point_description')
    list_filter=('product',)
    search_fields =['point_description',]

admin.site.register(ProductDetailedDescriptionPanelCheck, ProductDetailedDescriptionPanelCheckAdmin)

class HospitalAdmin(admin.ModelAdmin):
    list_display = ('hospital_name','address_line_1','phone','email', 'city', 'state')

admin.site.register(Hospital,HospitalAdmin)