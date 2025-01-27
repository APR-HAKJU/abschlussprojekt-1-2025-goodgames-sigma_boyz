


import pytest
import backend  # Stelle sicher, dass das Modul korrekt importiert ist

@pytest.fixture
def library():
    """Fixture to provide a fresh GameLibrary instance."""
    lib = backend.GameLibrary()
    lib.games = []  # Clear games for clean tests
    lib.next_id = 1
    return lib

def test_load_from_nonexistent_csv(library):
    library.csv_path = "nonexistent.csv"
    with pytest.raises(FileNotFoundError):
        library.load_from_csv()

def test_add_duplicate_game(library):
    library.add_game("Zelda", "Switch")
    with pytest.raises(ValueError):
        library.add_game("Zelda", "Switch")

def test_get_game_by_invalid_id(library):
    library.add_game("Zelda", "Switch")
    with pytest.raises(ValueError):
        library.get_game_by_id(999)
