"""Regression coverage for bulk responses containing one exception object."""

from types import SimpleNamespace

import pytest

from pinterest.utils.error_handling import verify_api_response
from pinterest.utils.sdk_exceptions import SdkException


@pytest.mark.parametrize("as_dict", [True, False], ids=["dict", "model"])
@pytest.mark.parametrize("as_list", [True, False], ids=["list", "single"])
def test_verify_api_response_rejects_bulk_exception(as_dict, as_list):
    exception = {"code": 1234, "message": "Test exception caught."}
    if not as_dict:
        exception = SimpleNamespace(**exception)
    exceptions = [exception] if as_list else exception
    item = {"exceptions": exceptions}
    response = {"items": [item]}
    if not as_dict:
        response = SimpleNamespace(items=[SimpleNamespace(**item)])

    with pytest.raises(SdkException, match="Test exception caught"):
        verify_api_response(response)
