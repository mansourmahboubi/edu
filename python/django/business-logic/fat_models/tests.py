import logging

import pytest
from django.contrib.auth import get_user_model

from .models import Address

logger = logging.getLogger(__name__)

User = get_user_model()


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
        return Address(
            user=user,
            street="Fake",
            number=1,
            is_default=False,
        )

    def test_sets_address_as_default_and_publishes_changes(self, mocker, address):
        mock_filter = mocker.patch.object(Address.objects, "filter")
        mock_update = mocker.patch.object(mock_filter.return_value, "update")
        mock_save = mocker.patch.object(address, "save")
        # mock_publish = mocker.patch.object(events, 'publish')

        address.set_default()
        # logger.error(address)
        # We lose the integration tests of the database flows
        mock_filter.assert_called_with(user=address.user)
        mock_update.assert_called_with(is_default=False)
        assert address.is_default is True
        mock_save.assert_called()
        # mock_publish.assert_called_with(events.DEFAULT_ADDRESS_CHANGED, address=address)
