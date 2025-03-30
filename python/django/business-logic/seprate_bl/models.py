from django.contrib.auth import get_user_model
from django.db import models

from .manager import AddressManager

User = get_user_model()


class Address(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="seprate_login_user"
    )
    street = models.CharField(max_length=50)
    number = models.PositiveIntegerField()
    is_default = models.BooleanField()

    @property
    def full_address(self):
        return f"{self.street}, {self.number}"

    objects = AddressManager()
