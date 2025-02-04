# backend.py

from datetime import datetime
import csv


class Game:
    """Represents a single game in the collection"""

    def __init__(self, id, title, platform, status="Want to Play", genre="Action"):
        """Initialize a new game"""
        self.id = id
        self.title = title
        self.platform = platform
        self.status = status
        self.rating = None
        self.genre = genre
        self.review = None
        self.date_added = datetime.now().date()
        self.completion_date = None

    def update(self, status=None, rating=None,genre=None, review=None):
        """Update game information"""
        if status:
            self.status = status
            self.completion_date = datetime.now().date() if status == "Completed" else None
        if rating is not None:  # Allow 0 as a rating
            self.rating = rating
        if genre is not None:
            self.genre = genre
        if review is not None:
            self.review = review


    def to_dict(self):
        """Convert game object to dictionary for frontend use"""
        return {
            'id': self.id,
            'title': self.title,
            'platform': self.platform,
            'status': self.status,
            'rating': self.rating,
            "genre": self.genre,
            'review': self.review,
            'date_added': self.date_added,
            'completion_date': self.completion_date
        }


class GameLibrary:
    """Manages the in-memory game collection"""

    def __init__(self):
        """Initialize empty game library"""
        self.games = []
        self.load_from_csv()
        self.next_id = 1
        self.csv_path = "./games.csv"

    def save_to_csv(self, game):
        """Save a game to the CSV file."""
        try:
            with open("games.csv", "a", newline="\n") as file:
                writer = csv.writer(file)
                writer.writerow([
                    game.id, game.title, game.platform, game.status, game.rating, game.genre,
                    game.review, game.date_added, game.completion_date
                ])
        except FileNotFoundError:
            print(f"Fehler: Datei {self.csv_path} wurde nicht gefunden.")
            raise

    def load_from_csv(self):
        """Load games from the CSV file."""
        try:
            with open("games.csv", "r", newline="\n") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                self.games = []
                highest_id = 0
                for row in reader:
                    if row and row[0].isdigit():
                        game = Game(
                            id=int(row[0]),
                            title=row[1],
                            platform=row[2],
                            status=row[3],
                            genre=row[5],
                        )
                        game.rating = (row[4]) if row[4] else None
                        game.review = row[6] if row[6] else None
                        game.date_added = datetime.strptime(row[7], "%Y-%m-%d").date() if row[7] else None
                        game.completion_date = datetime.strptime(row[8], "%Y-%m-%d").date() if row[8] else None
                        self.games.append(game)
                        highest_id = max(highest_id, game.id)
                self.next_id = highest_id + 1  # Update next_id after loading all games
        except FileNotFoundError:
            print(f"Fehler: Datei {self.csv_path} wurde nicht gefunden.")
            self.games = []
            self.next_id = 1  # Set to 1 if the file doesn't exist

    def update_game_in_csv(self, game):
        """Update the corresponding row in the CSV file."""
        game_list = []
        try:
            with open("games.csv", "r", newline="\n") as file:
                reader = csv.reader(file)
                header = next(reader)
                for row in reader:
                    if row and row[0].isdigit():
                        current_game = Game(
                            id=int(row[0]),
                            title=row[1],
                            platform=row[2],
                            status=row[3],
                            genre=row[5],
                        )
                        current_game.rating = (row[4]) if row[4] else None
                        current_game.review = row[6] if row[6] else None
                        current_game.date_added = datetime.strptime(row[7], "%Y-%m-%d").date() if row[7] else None
                        current_game.completion_date = datetime.strptime(row[8], "%Y-%m-%d").date() if row[8] else None
                        if current_game.id == game.id:
                            current_game = game
                        game_list.append(current_game.to_dict())

            with open("games.csv", "w", newline="\n") as file:
                writer = csv.DictWriter(file,
                                        fieldnames=["id", "title", "platform", "status", "rating", "genre", "review", "date_added",
                                                    "completion_date"])
                writer.writeheader()
                writer.writerows(game_list)
        except ValueError as e:
            print("Es ist ein Fehler aufgetreten")
            raise e


        # TODO: Add a try except block to handle the case where the file does not exist
        pass

    def add_game(self, title, platform, status="Want to Play", genre="Action"):
        """Add a new game to the library."""
        try:
            with open("games.csv", "r", newline="\n") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                games = []
                highest_id = 0
                for row in reader:
                    if row and row[0].isdigit():
                        game = Game(
                            id=int(row[0]),
                            title=row[1],
                            platform=row[2],
                            status=row[3],
                            genre=row[5]
                        )
                        game.rating = (row[4]) if row[4] else None
                        game.review = row[6] if row[6] else None
                        game.date_added = datetime.strptime(row[7], "%Y-%m-%d").date() if row[7] else None
                        game.completion_date = datetime.strptime(row[8], "%Y-%m-%d").date() if row[8] else None
                        games.append(game)
                        highest_id = max(highest_id, game.id)
                self.next_id = highest_id + 1  # Update next_id after loading all games
            for game in self.games:
                if game.title == title:
                    raise ValueError(f"Spiel mit dem Titel '{title}' existiert bereits.")
            new_game = Game(
                id=self.next_id,
                title=title,
                platform=platform,
                status=status,
                genre=genre,
            )
            self.save_to_csv(new_game)
            self.games.append(new_game)
            #self.next_id += 1
            return new_game.to_dict()
        except ValueError as e:
            print(f"Fehler: {e}")
            raise
    def update_game(self, game_id, status, genre,rating=None,review=None):
        """Update an existing game's information"""
        for game in self.games:
            if game.id == game_id:  # Use object attribute
                game.update(status,rating, genre, review)
                self.update_game_in_csv(game)
                return game.to_dict()
        return None
    def get_game_by_name(self, name=None):
        if name and name == name:
            filtered_games = [game for game in self.games if game.title == name]
        else:
            filtered_games = self.games
        return [game.to_dict() for game in filtered_games]
    def get_games(self, status=None):
        """Get games, optionally filtered by status"""
        if status and status != "All":
            filtered_games = [game for game in self.games if game.status == status]  # Use object attribute
        else:
            filtered_games = self.games
        return [game.to_dict() for game in filtered_games]

    def get_game_by_id(self, game_id):
        """Get a specific game by its ID."""
        try:
            for game in self.games:
                if game.id == game_id:
                    return game.to_dict()
            raise ValueError(f"Spiel mit der ID '{game_id}' wurde nicht gefunden.")
        except ValueError as e:
            print(f"Fehler: {e}")
            raise