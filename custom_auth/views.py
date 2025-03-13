from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
import uuid
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomAuthenticationForm

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True  # El usuario estará activo pero no verificado
            user.verification_token = uuid.uuid4()
            user.save()
            
            # Enviar correo de verificación
            current_site = get_current_site(request)
            mail_subject = 'Confirma tu cuenta'
            message = render_to_string('account/verification_email.html', {
                'user': user,
                'domain': current_site.domain,
                'token': user.verification_token,
            })
            send_mail(mail_subject, message, 'noreply@tudominio.com', [user.email])
            
            messages.success(request, 'Por favor, confirma tu correo electrónico para completar el registro.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'account/signup.html', {'form': form})

def verify_email(request, token):
    try:
        user = CustomUser.objects.get(verification_token=token)
        user.is_email_verified = True
        user.save()
        messages.success(request, 'Tu correo ha sido verificado. Ahora puedes iniciar sesión.')
        return redirect('login')
    except CustomUser.DoesNotExist:
        messages.error(request, 'El enlace de verificación no es válido.')
        return redirect('login')

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # username field contiene el email
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                if user.is_email_verified:
                    login(request, user)
                    return redirect('products:dashboard')
                else:
                    messages.error(request, 'Por favor, verifica tu correo electrónico antes de iniciar sesión.')
            else:
                messages.error(request, 'Correo o contraseña incorrectos.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'account/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    return render(request, 'account/dashboard.html')