from django.conf import settings
from django.db import models


class Address(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    street = models.CharField(max_length=50)
    number = models.PositiveIntegerField()
    is_default = models.BooleanField()

    @property
    def full_address(self):
        return f"{self.street}, {self.number}"

    # Business logic inside the model
    def set_default(self):
        # Dependencies with other models (in this case the same one)
        Address.objects.filter(user=self.user).update(is_default=False)
        self.is_default = True
        self.save()

        # Side-effects of the action inside the model, SRP ko
        # events.publish(events.DEFAULT_ADDRESS_CHANGED, address=self)

    def __str__(self):
        return f"{self.user}-{self.street}"
