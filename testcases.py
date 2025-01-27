import pytest
import backend


def test_load_from_nonexistent_csv():
    library = backend.GameLibrary()
    library.csv_path = "nonexistent.csv"
    with pytest.raises(FileNotFoundError):
        library.load_from_csv()

def test_add_duplicate_game():
    library = backend.GameLibrary()
    library.add_game("Zelda", "Switch")
    with pytest.raises(ValueError):
        library.add_game("Zelda", "Switch")

def test_get_game_by_invalid_id():
    library = backend.GameLibrary()
    library.add_game("Zelda", "Switch")
    with pytest.raises(ValueError):
        library.get_game_by_id(999)
