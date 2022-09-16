import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase

from .business_logic import set_default
from .models import Address

User = get_user_model()


@pytest.mark.django_db
class TestAddressManagerSetDefault:
    @pytest.fixture
    def saved_user(self):
        user = User.objects.create(
            first_name="test",
            last_name="test last name",
            email="asdf-2@email.com",
            username="asdf-2@email.com",
        )
        return user

    # We make integration tests for the manager to validate database behaviours
    def test_sets_address_as_default(self, saved_user):
        old_default_address = Address.objects.create(
            user=saved_user, street="Fake", number=1, is_default=True
        )
        address = Address.objects.create(
            user=saved_user, street="Fake", number=2, is_default=False
        )

        Address.objects.set_default(address)  # type: ignore

        old_default_address.refresh_from_db()
        address.refresh_from_db()
        assert not old_default_address.is_default
        assert address.is_default


class TestSetDefault:
    @pytest.fixture
    def user(self):
        return User(
            first_name="test",
            last_name="test last name",
            email="asdf@email.com",
            username="asdf@email.com",
        )

    @pytest.fixture
    def address(self, user):
        return Address(user=user, street="Fake", number=1, is_default=False)

    def test_sets_address_as_default_and_publishes_changes(self, mocker, address):
        # In this case a lot less dependencies
        mock_set_default = mocker.patch.object(Address.objects, "set_default")
        # mock_publish = mocker.patch.object(events, 'publish')

        set_default(address)

        # We test only the logic and forget about ORM interactions
        mock_set_default.assert_called_with(address)
        # mock_publish.assert_called_with(events.DEFAULT_ADDRESS_CHANGED, address=address)
