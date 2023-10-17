from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    
    @property
    def cart_id(self):
        return self.id
    
    @classmethod
    def create_user(cls, first_name, last_name, email, password):
        try:
            # Check if a user with the given email already exists
            existing_user = cls.objects.get(email=email)
            return existing_user  # Return the existing user if found
        except cls.DoesNotExist:
            # If the user doesn't exist, create a new user
            new_user = cls(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            
            new_user.save()
            return new_user
    
    @classmethod
    def get_user(cls, email):
        try:
            existing_user = cls.objects.get(email=email)
            return existing_user  # Return the existing user if found
        except cls.DoesNotExist:
            return "Not a valid user"
    
    def __str__(self):
        return self.email