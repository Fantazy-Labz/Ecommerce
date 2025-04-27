# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import uuid
from django.template.loader import render_to_string
from django.core.mail import send_mail

class CustomUser(AbstractUser):
    name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(_('email address'), unique=True)
    is_email_verified = models.BooleanField(default=False)
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    profile_picture = models.ImageField(upload_to='profile_pic', default='default_profile.jpg')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
    
    def send_verification_email(self):
        """
        Envía un correo electrónico de verificación al usuario.
        """
        subject = 'Verifica tu correo electrónico'
        
        # Renderizar el template HTML con el contexto
        message_html = render_to_string('../templates/account/verification_email.html', {
            'user': self,
            'token': self.verification_token,
            'domain': settings.BASE_URL or 'http://localhost:8000'
        })
        
        # Versión de texto plano para clientes que no soportan HTML
        message_text = f"""
        Hola {self.username},
        
        Gracias por registrarte. Por favor, verifica tu dirección de correo electrónico haciendo clic en el siguiente enlace:
        
        {settings.BASE_URL or 'http://localhost:8000'}/custom_auth/verify-email/{self.verification_token}/
        
        Si no has solicitado este registro, puedes ignorar este correo.
        
        Saludos,
        El equipo de tu Ecommerce
        """
        
        # Enviar el correo
        try:
            send_mail(
                subject,
                message_text,
                settings.EMAIL_HOST_USER,
                [self.email],
                html_message=message_html,
                fail_silently=False,
            )
            return True
        except Exception as e:
            print(f"Error al enviar el correo: {str(e)}")
            return False