from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


# Create Model Class Here

class Profile(models.Model):
    objects = None
    staff = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    email = models.EmailField(max_length=30, null=True)
    phone = models.CharField(max_length=10, null=True, validators=[
        RegexValidator(
            regex='^[0-9]*$',
            message='Contact No can only contain numbers',
            code='Invalid Contact No '
        ),
        RegexValidator(
            regex='^.{10}$',
            message='Contact No length is invalid',
            code='Invalid Contact No ',
        )
    ])
    first_name = models.CharField(max_length=15, null=True)
    last_name = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'{self.staff.username}-Profile'
