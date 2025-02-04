import unittest
from backend import GameLibrary


class TestGameLibrary(unittest.TestCase):
    def setUp(self):
        """Initialisiere eine neue GameLibrary für jeden Test."""
        self.library = GameLibrary()
        self.library.games = []  # Leere die Bibliothek für saubere Tests
        self.library.next_id = 1

    def test_add_game(self):
        """Testet das Hinzufügen eines neuen Spiels."""
        game = self.library.add_game("The Witcher 3", "PC")
        self.assertEqual(game['title'], "The Witcher 3")
        self.assertEqual(game['platform'], "PC")
        self.assertEqual(game['status'], "Want to Play")
        self.assertEqual(len(self.library.games), 1)

    def test_update_game(self):
        """Testet das Aktualisieren eines Spiels."""
        game = self.library.add_game("Dark Souls", "PS4")
        game_id = game['id']
        self.library.update_game(game_id, status="Completed", rating=9,genre="Action" ,review="Ein großartiges Spiel!")
        updated_game = self.library.get_game_by_id(game_id)
        self.assertEqual(updated_game['status'], "Completed")
        self.assertEqual(updated_game['genre'], "Action")
        self.assertEqual(updated_game['rating'], 9)
        self.assertEqual(updated_game['review'], "Ein großartiges Spiel!")

    def test_get_game_by_id(self):
        """Testet das Abrufen eines Spiels per ID."""
        game = self.library.add_game("Cyberpunk 2077", "PC")
        game_id = game['id']
        fetched_game = self.library.get_game_by_id(game_id)
        self.assertEqual(fetched_game['title'], "Cyberpunk 2077")
        self.assertEqual(fetched_game['platform'], "PC")


if __name__ == "__main__":
    unittest.main()