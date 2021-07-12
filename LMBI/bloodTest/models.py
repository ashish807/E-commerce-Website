from django.db import models

# Create your models here.


# class BloodTestCategory(models.Model):
#     BTcategory_name      = models.CharField(max_length=200, unique=True)
#     slug              = models.SlugField(max_length=200, unique=True)
#     #category          = models.ForeignKey(Category, on_delete=models.CASCADE) 
#     product_description = models.TextField(max_length=5000, blank=True)
#     price             = models.IntegerField()
#     image             = models.ImageField(upload_to='photos/products')
#     stock             = models.IntegerField()
#     is_available      = models.BooleanField(default=True)
#     pincode_delivery_check = models.TextField(max_length=200, blank=True)
#     warranty_details = models.TextField(max_length=200, blank=True)
#     detailed_description_panel = models.TextField(max_length=600, blank=True)




#     created_date      = models.DateTimeField(auto_now_add=True)
#     modified_date     = models.DateTimeField(auto_now=True)



#     def averageReview(self):
#         reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average = Avg('rating'))
#         avg =0
#         if reviews['average'] is not None:
#             avg = float(reviews['average'])
#         return avg
    
#     def countReview(self):
#         reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
#         count =0
#         if reviews['count'] is not None:
#             count = int(reviews['count'])
#         return count


#     def get_url(self):
#         return reverse('product_detail', args=[self.category.slug, self.slug])

#     def __str__(self):
#         return self.product_name