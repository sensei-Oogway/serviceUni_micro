from django.db import models

class Medicines(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    @classmethod
    def get_all_medicines(cls):
        return cls.objects.all()

    def __str__(self):
        return self.name

def __str__(self):
        return self.name

class Cart(models.Model):
    id = models.IntegerField(primary_key=True)
    medicine_ids = models.JSONField(default=list, blank=True)
    #medicine_ids = models.ManyToManyField('pharmacy.Medicines')

    @classmethod
    def add_medicine_to_cart(cls, cart_id, medicine_id):
        try:
            cart = cls.objects.get(pk=cart_id)            
            cart.medicine_ids.append(medicine_id)
            cart.save()
            
            return True
        except Cart.DoesNotExist:
            return False  # Cart not found