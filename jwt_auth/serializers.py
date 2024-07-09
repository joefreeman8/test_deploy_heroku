from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    # validate the passwords matching
    # hash password
    # add the to database
    def validate(self, data): # <- data comes from request.body
        password = data.pop('password')
        password_confirmation = data.pop('password_confirmation')

        # check match
        if password != password_confirmation:
            raise ValidationError({'password_confirmation': 'passwords do not match'})
        
        # validate
        try:
            password_validation.validate_password(password=password)
        except ValidationError as err:
            raise ValidationError({'password': err.messages})
        
        # hash password
        data['password'] = make_password(password)

        return data
    
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'profile_image', 'password', 'password_confirmation')


