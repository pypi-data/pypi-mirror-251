import pytest
import unittest

from promptflow.connections import CustomConnection
from promptflow_clinical_rwd.tools.clinical_note_summarization import clinical_rwd


@pytest.fixture
def my_custom_connection() -> CustomConnection:
    my_custom_connection = CustomConnection(
        {
            "api-key" : "my-api-key",
            "api-secret" : "my-api-secret",
            "api-url" : "my-api-url"
        }
    )
    return my_custom_connection


class TestTool:
    def test_clinical_rwd(self, my_custom_connection):
        result = clinical_rwd(my_custom_connection, input_text="Microsoft")
        assert result == "Hello Microsoft"


# Run the unit tests
if __name__ == "__main__":
    unittest.main()