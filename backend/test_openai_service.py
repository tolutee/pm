import os
import pytest
from unittest.mock import patch, MagicMock
from openai_service import get_openai_client, simple_math_calculation


def test_get_openai_client_missing_key():
    """Test that missing API key raises ValueError."""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="OPENAI_API_KEY"):
            get_openai_client()


def test_get_openai_client_with_key():
    """Test that OpenAI client is created when API key is present."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        client = get_openai_client()
        assert client is not None
        assert client.api_key == "test-key"


@patch("openai_service.get_openai_client")
def test_simple_math_calculation_success(mock_get_client):
    """Test successful math calculation."""
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "4"
    mock_client.chat.completions.create.return_value = mock_response
    
    result = simple_math_calculation("2+2")
    
    assert result == "4"
    mock_client.chat.completions.create.assert_called_once()
    call_args = mock_client.chat.completions.create.call_args
    assert call_args[1]["model"] == "gpt-4o"
    assert "2+2" in call_args[1]["messages"][0]["content"]


@patch("openai_service.get_openai_client")
def test_simple_math_calculation_api_error(mock_get_client):
    """Test that API errors are properly wrapped."""
    mock_client = MagicMock()
    mock_get_client.return_value = mock_client
    mock_client.chat.completions.create.side_effect = Exception("API failed")
    
    with pytest.raises(RuntimeError, match="OpenAI API error"):
        simple_math_calculation("2+2")
