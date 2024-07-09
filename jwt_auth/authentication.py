from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt

User = get_user_model()

# Extend the Basic Authentication
# as it already has password and email authentication

class JWTAuthentication(BasicAuthentication):

    def authenticate(self, request):
        header = request.headers.get('Authorization')

        if not header:
            return None
        
        if not header.startswith('Bearer'):
            raise PermissionDenied(detail="Invalid Auth Token")
        
        token = header.replace('Bearer ', '')

        try:
            # make payload
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            # get user id from payload.sub
            user = User.objects.get(pk=payload.get('sub'))
            print("USER -> ", user)

        # incase token has expired or is incorrect formatting
        except jwt.exceptions.InvalidTokenError:
            raise PermissionDenied(detail="Invalid Token")
        
        except User.DoesNotExist:
            raise PermissionDenied(detail="User not found")
        

        # If everything is good, return user & token
        # This becomes accessable in our views under request.user and request.token
        return (user, token)


