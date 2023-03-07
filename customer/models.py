from django.db import models

# Create your models here.
class MenuItem(models.Model):
    name= models.CharField(max_length=100)
    description=models.TextField()
    image = models.ImageFeild(upload_to='menu_image/')
    price = models.DecimalFeild(max_digits=5, decimal_place=2)
    category =models.ManyToManyField('Category',related_name='item')

    def __str__(self) -> str:
        return super().__str__()

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return super().__str__()
    
class OrderModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    price = models.DecimalFeild(max_digits=7, decimal_places=2)
    items = models.ManyToManyField('MenuItem', related_name='orer', blank=True)

    def __str__(self) -> str:
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p")}'

