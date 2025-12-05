import os
import pytest

if os.getenv("CI") == "true":
    pytest.skip("Skipping DB tests on CI", allow_module_level=True)
#Only skip DB tests when running on CI