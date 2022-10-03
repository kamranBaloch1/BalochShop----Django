

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime    

# Create your models here.


# STATE_CHOICES=(


#     ("Turbat","Turbat"),
#     ("Gwadar","Gwadar"),
#     ("Pasni","Pasni"),
#     ("Panjgoor","Panjgoor"),
#     ("Jewani","Jewani"),
#     ("Keach","Keach"),
#     ("Sibi","Sibi"),
#     ("DG khan","DG khan"),
#     ("Tump","Tump"),
# )


class Customer(models.Model):
   user = models.ForeignKey(User,on_delete=models.CASCADE)
   name= models.CharField(max_length=200)
   address = models.CharField(max_length=200,default="")
   address2 = models.CharField(max_length=200,default="")
   city= models.CharField(max_length=200)
   zipcode= models.IntegerField()
   state=models.CharField(max_length=100)

   def __str__(self) -> str:
      return self.name


CATERGORY_CHOSICES =(

        ("TW","Top wear"),
        ("BW","Bottom wear"),
        ("M","Mobiles"),
        ("L","Laptop"),
      )
     

class Product(models.Model):
   
    title = models.CharField(max_length=200)
    price = models.FloatField()
    discount=models.FloatField()
    description = models.TextField(max_length=4000)
    brand= models.CharField(max_length=100)
    category = models.CharField(choices=CATERGORY_CHOSICES,max_length=50)
    product_img= models.ImageField(upload_to = "productImg")

    def __str__(self) -> str:
       return self.title

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1,)
    date = models.DateTimeField(default=datetime.now(), blank=True)

    def __str__(self) -> str:
       return str(self.id)

    @property
    def total_coast(self):
        return self.quantity * self.product.discount


ORDER_STATUS=(
    ("Pending","Pending"),
    ("Delevired","Delevired"),
    ("On The Way","On The Way"),
    ("Packed","Packed"),
    ("Cancel","Cancel"),
)


class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    costumer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=ORDER_STATUS,default="Pending",max_length=100)

    def __str__(self) -> str:
       return str(self.id)
    @property
    def total_coast(self):
        return self.quantity * self.product.discount
   
   


