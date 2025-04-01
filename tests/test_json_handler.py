import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
    )

# False error due to format + runtime correction
from unittest.mock import mock_open, patch
from json_handler import load_quotes, save_quotes, is_valid_keyword, add_quotes


def test_load_quotes():
    quotes = load_quotes("test_quotes.json")
    assert isinstance(quotes, dict)


def test_load_quotes_file_not_found():
    quotes = load_quotes("non_existent_file.json")
    assert quotes == {}


def test_load_quotes_unexpected_error():
    with patch("builtins.open", side_effect=Exception("Random error")):
        quotes = load_quotes("test_quotes.json")
        assert quotes == {}


def test_add_quotes():
    # Mock file handling
    with patch("builtins.open", mock_open(read_data='{}')) as mock_file, \
         patch("json.dump") as mock_dump:
        add_quotes("test_quotes.json", "funny", ["You are.", "No, you are."])
        mock_file.assert_called_with("test_quotes.json", "w")
        mock_dump.assert_called_once_with(
            {"funny": ["You are.", "No, you are."]}, mock_file(), indent=4)


def test_is_valid_keyword():
    testKeyword1 = "brain"
    testKeyword2 = "raWRxDD"
    testKeyword3 = "54nap"
    testKeyword4 = "hey-@$$"
    assert is_valid_keyword(testKeyword1)
    assert is_valid_keyword(testKeyword2)
    assert not is_valid_keyword(testKeyword3)
    assert not (is_valid_keyword(testKeyword4))


def test_save_quotes():
    quotes = {
        "Cook": ["Burnt the kitchen.", "Eggs and bacon."],
        "Rain": ["It's pouring.", "Yellow rainboots."]
        }
    with patch("builtins.open", mock_open(read_data='{}')) as mock_file, \
         patch("json.dump") as mock_dump:
        save_quotes("test_quotes.json", quotes)
        mock_file.assert_called_with("test_quotes.json", "w")
        mock_dump.assert_called_once_with(
            {
                "Cook": ["Burnt the kitchen.", "Eggs and bacon."],
                "Rain": ["It's pouring.", "Yellow rainboots."]
            }, mock_file(), indent=4
        )


def test_save_quotes_file_not_found(capfd):
    quotes = {
        "Rain": ["It's pouring.", "Yellow rainboots."]
        }
    with patch("builtins.open", side_effect=FileNotFoundError):
        save_quotes("test_file_not_found.json", quotes)
    captured = capfd.readouterr()
    assert (
        "Error: File not found"
    ) in captured.out


def test_save_quotes_unexpected_error(capfd):
    quotes = {
        "Rain": ["It's pouring.", "Yellow rainboots."]
        }
    with patch("builtins.open", side_effect=Exception("Random error")):
        save_quotes("test_file_not_found.json", quotes)
    captured = capfd.readouterr()
    assert (
        "An unexpected error occurred: Random error"
    ) in captured.out
