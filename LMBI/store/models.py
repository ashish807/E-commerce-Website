from django.contrib.auth.models import update_last_login
from django.db import models
from category.models import Category
from django.urls import reverse
from accounts.models import Account, AddState
from django.db.models import Avg, Count
# Create your models here.
 

class Product(models.Model):
    product_name      = models.CharField(max_length=200, unique=True)
    slug              = models.SlugField(max_length=200, unique=True)
    category          = models.ForeignKey(Category, on_delete=models.CASCADE) 
    product_description = models.TextField(max_length=500, blank=True)
    price             = models.IntegerField()
    image             = models.ImageField(upload_to='photos/products')
    stock             = models.IntegerField()
    is_available      = models.BooleanField(default=True)
    pincode_delivery_check = models.TextField(max_length=200, blank=True)
    warranty_details = models.TextField(max_length=200, blank=True)
    detailed_description_panel = models.TextField(max_length=600, blank=True)




    created_date      = models.DateTimeField(auto_now_add=True)
    modified_date     = models.DateTimeField(auto_now=True)



    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average = Avg('rating'))
        avg =0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg
    
    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count =0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count


    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name




class ProductDetailedDescriptionPanelCheck(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    point_description = models.TextField(max_length=200, blank=True)
    
    def __str__(self):
        return self.point_description



class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)
    
    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)
    



variation_category_choice=(
    ('color','color'),
    ('size','size'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices = variation_category_choice)
    variation_value =  models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()
    
    def __str__(self):
        return self.variation_value



class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip =models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class  ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to ='store/products', max_length=255)

    def __str__(self):
        return self.product.product_name
    
    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural ='product gallery'


class BloodCategory(models.Model):
    category_name = models.CharField(max_length=100)
    category_price = models.IntegerField()
    
    def __str__(self):
        return self.category_name


class Hospital(models.Model):
    hospital_name = models.CharField(max_length=100)
    address_line_1 = models.TextField(max_length=100)
    address_line_2 = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)

    def __str__(self):
        return self.hospital_name


class Appointments(models.Model):
    report = models.FileField(blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True)
    total_amount = models.IntegerField(blank=True, null=True)
    blood_category = models.TextField(max_length=1000, blank=True, null=True)
    blood_category_detail = models.TextField(max_length=1000, blank=True, null=True)
    appointment_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    state = models.ForeignKey(AddState, on_delete=models.SET_NULL, null=True)
    city = models.CharField(max_length=50)
    # time_slot =  models.TextField(max_length=100, blank=True, null = True)
    date = models.DateField(blank=True, null = True)
    time = models.TimeField(blank=True, null=True)
    ip = models.CharField(blank=True, max_length=20)
    
    # is_appointed = models.BooleanField(default=False)
    
    appointment_request_date = models.DateTimeField(auto_now_add=True)
    is_billed = models.BooleanField(default=False)

    vendorConfirmation = models.BooleanField(default=False, null=False)
    bloodCollected = models.BooleanField(default=False, null=False)
    bloodAnalysed = models.BooleanField(default=False, null=False)
    reportUploaded = models.BooleanField(default=False, null=False)
    # checked_and_ready_for_shipping = models.BooleanField(default=False, null=True)
    
    # delivery_guy_checked = models.BooleanField(default=False, null=True)
    
    # appointment_recieved_by_client = models.BooleanField(default=False, null=True)

    'vendorConfirmation','bloodCollected','bloodAnalysed', 'reportUploaded'
 
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
 
    def get_full_address(self):
        return f'{self.address_line_1}{self.address_line_2}'