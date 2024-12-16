import pytest
import os
import csv
from WordGame import ensure_csv_files_exist, read_category_from_csv, append_to_category_csv

# Test Data
TEST_CATEGORIES = ["animals", "things", "plants"]
TEST_WORDS = {
    "animals": ["dog", "cat", "elephant"],
    "things": ["chair", "table", "computer"],
    "plants": ["rose", "oak", "cactus"],
}

@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Fixture to ensure a clean test environment before and after each test."""
    # Remove test files if they exist
    for category in TEST_CATEGORIES:
        if os.path.exists(f"{category}.csv"):
            os.remove(f"{category}.csv")
    yield
    # Cleanup after tests
    for category in TEST_CATEGORIES:
        if os.path.exists(f"{category}.csv"):
            os.remove(f"{category}.csv")

def test_ensure_csv_files_exist():
    """Test if CSV files are created successfully."""
    ensure_csv_files_exist()
    for category in TEST_CATEGORIES:
        assert os.path.exists(f"{category}.csv")
        with open(f"{category}.csv", mode="r") as file:
            reader = csv.reader(file)
            header = next(reader)
            assert header == ["Word"]  # Check if header is correct

def test_read_category_from_csv_empty():
    """Test reading from an empty CSV file."""
    ensure_csv_files_exist()
    for category in TEST_CATEGORIES:
        words = read_category_from_csv(category)
        assert words == []  # Should return an empty list

def test_append_to_category_csv():
    """Test appending words to a category CSV file."""
    ensure_csv_files_exist()
    for category, words in TEST_WORDS.items():
        append_to_category_csv(category, words)
        # Verify the contents of the CSV file
        with open(f"{category}.csv", mode="r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            csv_words = [row[0] for row in reader]
            assert csv_words == words

def test_read_category_from_csv_with_words():
    """Test reading words from a populated CSV file."""
    ensure_csv_files_exist()
    for category, words in TEST_WORDS.items():
        append_to_category_csv(category, words)
        read_words = read_category_from_csv(category)
        assert read_words == words
