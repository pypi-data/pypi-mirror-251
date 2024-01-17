from __future__ import annotations

from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from django_afip import models
from django_afip.factories import ReceiptFactory


@pytest.fixture()
def disable_durability_check() -> None:
    """Disable the global fixture of the same name."""


@pytest.mark.django_db()
def test_raises() -> None:
    """Calling ``validate`` inside a transaction should raise."""

    receipt = ReceiptFactory()
    queryset = models.Receipt.objects.filter(pk=receipt.pk)
    ticket = MagicMock()

    with patch(
        "django_afip.models.ReceiptQuerySet._assign_numbers",
        spec=True,
    ) as mocked_assign_numbers, patch(
        "django_afip.models.ReceiptQuerySet._validate",
        spec=True,
    ) as mocked__validate, pytest.raises(
        RuntimeError
    ):
        # TYPING: django-stubs can't handle methods in querysets
        queryset.validate(ticket)  # type: ignore[attr-defined]

    assert mocked_assign_numbers.call_count == 0
    assert mocked__validate.call_count == 0
    assert mocked__validate.call_args is None
