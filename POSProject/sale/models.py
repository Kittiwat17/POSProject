from django.db import models


# Create your models here.
class Type(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    
class Product(models.Model):
    name = models.CharField(max_length=50)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
    price = models.IntegerField(default=1)
    amount = models.IntegerField(default=0)


#    text = models.TextField()
#    SINGLE = '01'
#    MULTIPLE = '02'
#    TYPES = (
#        (SINGLE, 'Single answer'),
#        (MULTIPLE, 'Multiple answer')
#    )
#   question_type = models.CharField(max_length=2, choices=TYPES, default='01')
#    poll = models.ForeignKey(Poll, on_delete=models.PROTECT)

#    def __str__(self):
#       return '(%s) %s' % (self.poll.title, self.text)

class Order(models.Model):
    date_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    total_price = models.IntegerField(default=0)
    # in_cart = models.BooleanField(default=False)
   

class Order_Products(models.Model):
    order_id = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    # in_cart = models.BooleanField(default=False)

  
#    def __str__(self):
#        return '(%s) %s' % (self.question.text, self.text)



