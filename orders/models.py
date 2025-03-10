from django.db import models

# Create your models here.
#Bag class for products selection
class Bag(model.Models):
    products = models.ForeignKey(Product,  on_delete=models.CASCADE)
    price = models.IntegerField(total_price)
    username = models.ForeingKey(Profile, on_delete = models.CASCADE)
    quantity = models.IntegerField(products_quant)

    def total_price(self):
        return self.quantity * self.product.price

    def products_quant(products):
        return  self.queantity

#Shipping model for shiping information
class ShippingInfo(model.Models):

    STATE_CHOICES = [
    ('AGU', 'Aguascalientes'),
    ('BCN', 'Baja California'),
    ('BCS', 'Baja California Sur'),
    ('CAM', 'Campeche'),
    ('CHP', 'Chiapas'),
    ('CHH', 'Chihuahua'),
    ('CMX', 'Ciudad de México'),
    ('COA', 'Coahuila'),
    ('COL', 'Colima'),
    ('DUR', 'Durango'),
    ('GUA', 'Guanajuato'),
    ('GRO', 'Guerrero'),
    ('HID', 'Hidalgo'),
    ('JAL', 'Jalisco'),
    ('MEX', 'Estado de México'),
    ('MIC', 'Michoacán'),
    ('MOR', 'Morelos'),
    ('NAY', 'Nayarit'),
    ('NLE', 'Nuevo León'),
    ('OAX', 'Oaxaca'),
    ('PUE', 'Puebla'),
    ('QUE', 'Querétaro'),
    ('ROO', 'Quintana Roo'),
    ('SLP', 'San Luis Potosí'),
    ('SIN', 'Sinaloa'),
    ('SON', 'Sonora'),
    ('TAB', 'Tabasco'),
    ('TAM', 'Tamaulipas'),
    ('TLA', 'Tlaxcala'),
    ('VER', 'Veracruz'),
    ('YUC', 'Yucatán'),
    ('ZAC', 'Zacatecas'),
]

    STATUS = [
            ("Delivered"),
            ("On route"),
            ("Store"),
    ]
    street = models.CharField(max_length=30)
    house_num = models.IntegerField(editable=True)
    contact_num = models.ForeignKey(CustomUser, on_delete= models.CASCADE)
    state = models.CharField(max_length=20, choices=STATE_CHOICES)
    township = models.CharField(max_length=20)
    order_id = models.CharField(max_length=18)
    status = models.CharField(max_length=20, options = STATUS)

#Payment information
class PaymentInformation(model.Models):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    amount = mdoels.ForeignKey(Bag, on_delete= models.CASCADE)
    order_id = models.ForeignKey(ShippingInfo, on_delete= models.CASCADE)
    
#Stripe API ???
