from django.db import models


class AddressManager(models.Manager):

    # We use the manager as a data repository
    def set_default(self, address):
        self.filter(user=address.user).update(is_default=False)
        address.is_default = True
        address.save()
