from django.db import models
from .models import Profile, Bag, Order 

#stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentInformation(models.Model): 
    # Relación con el perfil del usuario
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='payments')

    # Relación con la bolsa de compras 
    bag = models.ForeignKey(Bag, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')

    # Relación con la orden (obligatoria)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')

    # Información del pago
    amount = models.DecimalField(max_digits=10, decimal_places=2)  
    currency = models.CharField(max_length=3, default='MXN')  
    payment_intent_id = models.CharField(max_length=100, unique=True)  
    payment_method = models.CharField(max_length=50)  
    status = models.CharField(max_length=20, default='pending')  

    def __str__(self):
        return f"Pago {self.payment_intent_id} - {self.amount} {self.currency}"

#def create_payment_intent(amount, currency='mxn'):
 #   try:
  #      intent = stripe.PaymentIntent.create(
   #         amount=amount,  # Monto en centavos
    #        currency=currency,
     #   )
      #  return intent
   # except stripe.error.StripeError as e:
    #    print(f"Error al crear el PaymentIntent: {e}")
     #   return None