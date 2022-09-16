from .models import Address


# The business rule is simple and easily testeable
def set_default(address):
    Address.objects.set_default(address)  # type: ignore
    # events.publish(events.DEFAULT_ADDRESS_CHANGED, address=address)
