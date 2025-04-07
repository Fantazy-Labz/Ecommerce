import json
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
import uuid
from .models import CustomUser
from django.views.decorators.csrf import csrf_exempt
                
@csrf_exempt
def registerView(request):
    if request.method != 'POST':
        return JsonResponse({
            "status": "error",
            "message": "Invalid request method"
        }, status=405)
    try:
        data = json.loads(request.body)
        email = data['email']
        password = data['password']

        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({
                "status": "error",
                "message": "Email already exists"
            }, status=400)

        verification_token = str(uuid.uuid4())
        user = CustomUser.objects.create_user(email=email, password=password, verification_token=verification_token)
        user.send_verification_email()

        return JsonResponse({
            "status": "success",
            "message": "User registered successfully. Please check your email to verify your account."
        })
    except KeyError as e:
        return JsonResponse({
            "status": "error",
            "message": f"Missing field: {str(e)}"
        }, status=400)

@csrf_exempt
def verifyEmail(token):
    try:
        user = CustomUser.objects.get(verification_token=token)
        user.is_email_verified = True
        user.save()
        return JsonResponse({
            "status": "success",
            "message": "Email verified successfully. You can now log in."
        })
    except CustomUser.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": "Invalid verification token"
        }, status=400)


@csrf_exempt
def loginView(request):  
        if request.method != 'POST':
            return JsonResponse({
                "status": "error",
                "message": "Invalid request method"
            }, status=405)
        try:
            data = json.loads(request.body)
            email = data['email']
            password = data['password']

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({
                    "status": "success",
                    "message": "Login successful"
                })
            else:
                return JsonResponse({
                    "status": "error",
                    "message": f"Missing field: {str(e)}"
                }, status=400)
        except KeyError as e:
            return JsonResponse({
                "status": "error",
                "message": f"Invalid credentials"
            }, status=401)

@csrf_exempt
def logoutView(request):
    if request.method == "¨POST":
        logout(request)
        return JsonResponse({
            "status": "success",
            "message": "Logout successful"
        })
    else:
        return JsonResponse({
            "status": "error",
            "message": "Invalid request method"
        }, status=405)

@csrf_exempt
@login_required
def upadateUser(request, user_id):
    if request.user.is_authenticated and request.user.is_suiperuser: 
        if request.method != "POST":
            return JsonResponse({
                "status": "error",
                "message": "Invalid request method"
            }, status=405)
        try:
            data = json.loads(request.body)
            user = CustomUser.objects.get(id=user_id)

            user.email = data.get('email', user.email)
            user.password = data.get('password', user.password)

            user.save()

            return JsonResponse({
                "status": "success",
                "message": "User updated successfully"
            })
        except CustomUser.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": "User not found"
            }, status=404)
    else:
        return JsonResponse({
            "status": "error",
            "message": "You are not authorized to perform this action"
        }, status=403)

@csrf_exempt
def deleteUser(request, user_id):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method != "DELETE":
            return JsonResponse({
                "status": "error",
                "message": "Invalid request method"
            }, status=405)
        try:
            user = CustomUser.objects.get(id=user_id)
            user.delete()
            return JsonResponse({
                "status": "success",
                "message": "User deleted successfully"
            })
        except CustomUser.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": "User not found"
            }, status=404)
    else:   
        return JsonResponse({
            "status": "error",
            "message": "You are not authorized to perform this action"
        }, status=403)

