from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
import uuid
from .models import CustomUser
from .serializers import CustomUserSerializer, UserLoginSerializer
from django.contrib.auth import authenticate, login, logout

@api_view(['POST'])
@permission_classes([AllowAny])
def registerView(request):
    """
    Registra un nuevo usuario.
    """
    try:
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            # Crear usuario pero no guardar aún
            user = serializer.save(is_active=True, is_email_verified=False)
            
            # Generar token de verificación y guardar
            verification_token = str(uuid.uuid4())
            user.verification_token = verification_token
            user.save()
            
            # Enviar email de verificación
            user.send_verification_email()
            
            return Response({
                "status": "success",
                "message": "Usuario registrado correctamente. Por favor verifica tu email."
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({
            "status": "error",
            "message": f"Error en el registro: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def verifyEmail(request, token):
    """
    Verifica el email de un usuario mediante el token enviado.
    """
    try:
        user = CustomUser.objects.get(verification_token=token)
        user.is_email_verified = True
        user.save()
        
        return Response({
            "status": "success",
            "message": "Email verificado correctamente. Ahora puedes iniciar sesión."
        })
    except CustomUser.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Token de verificación inválido."
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def loginView(request):
    """
    Autentica a un usuario y devuelve un token JWT.
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            if not user.is_email_verified:
                return Response({
                    "status": "error",
                    "message": "Por favor verifica tu email antes de iniciar sesión."
                }, status=status.HTTP_403_FORBIDDEN)
                
            login(request, user)
            
            # Aquí podrías generar y devolver un token JWT
            return Response({
                "status": "success",
                "message": "Inicio de sesión exitoso",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "last_name": user.last_name
                }
            })
        else:
            return Response({
                "status": "error",
                "message": "Credenciales inválidas."
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response({
        "status": "error",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logoutView(request):
    """
    Cierra la sesión del usuario actual.
    """
    logout(request)
    return Response({
        "status": "success",
        "message": "Sesión cerrada correctamente."
    })

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def updateUser(request, user_id=None):
    """
    Actualiza la información de un usuario.
    Si no se proporciona user_id, actualiza al usuario actual.
    """
    # Determinar qué usuario actualizar
    if user_id and request.user.is_superuser:
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Usuario no encontrado."
            }, status=status.HTTP_404_NOT_FOUND)
    elif user_id and not request.user.is_superuser:
        return Response({
            "status": "error",
            "message": "No tienes permiso para actualizar este usuario."
        }, status=status.HTTP_403_FORBIDDEN)
    else:
        user = request.user
    
    # Actualizar el usuario
    serializer = CustomUserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "status": "success",
            "message": "Usuario actualizado correctamente."
        })
    
    return Response({
        "status": "error",
        "errors": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, user_id):
    """
    Elimina un usuario (solo para administradores).
    """
    try:
        user = CustomUser.objects.get(id=user_id)
        email = user.email  # Guardar para mensaje
        user.delete()
        
        return Response({
            "status": "success",
            "message": f"Usuario {email} eliminado correctamente."
        })
    except CustomUser.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Usuario no encontrado."
        }, status=status.HTTP_404_NOT_FOUND)