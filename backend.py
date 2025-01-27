# backend.py

from datetime import datetime
import csv

class Game:
    """Represents a single game in the collection"""

    def __init__(self, id, title, platform, status="Want to Play"):
        """Initialize a new game"""
        self.id = id
        self.title = title
        self.platform = platform
        self.status = status
        self.rating = None
        self.review = None
        self.date_added = datetime.now().date()
        self.completion_date = None

    def update(self, status=None, rating=None, review=None):
        """Update game information"""
        if status:
            self.status = status
            self.completion_date = datetime.now().date() if status == "Completed" else None
        if rating is not None:  # Allow 0 as a rating
            self.rating = rating
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

    def save_to_csv(self,game):
        #TODO: Impement this method.
        # It should take a game object and save it as a row to a csv
        # the path of the csv is found in self.csv_path
        with open("./games.csv", "a", newline='\n') as file:
            writer = csv.writer(file)
            writer.writerow([game.id, game.title, game.platform, game.status, game.rating, game.review, game.date_added,
                            game.completion_date])
        #TODO: Add a try except block to handle the case where the file does not exist
        pass

    def load_from_csv(self):
        # TODO Implement this method.
        # It should load all objects from a csv file and return put the games into self.games
        # the path of the csv is found in self.csv_path
        with open("games.csv", "r", newline='\n') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            self.games = []
            highest_id = 0
            for row in reader:
                if row and row[0].isdigit():  # Skip empty and invalid rows
                    game = Game(
                        id=int(row[0]),
                        title=row[1],
                        platform=row[2],
                        status=row[3],
                    )
                    game.rating = float(row[4]) if row[4] else None
                    game.review = row[5] if row[5] else None
                    game.date_added = datetime.strptime(row[6], "%Y-%m-%d").date() if row[6] else None
                    game.completion_date = datetime.strptime(row[7], "%Y-%m-%d").date() if row[7] else None
                    self.games.append(game)
                    highest_id = max(highest_id, game.id)  # Track the highest existing ID
            self.next_id = highest_id + 1
            self.next_id = 1
        # TODO: Add a try except block to handle the case where the file does not exist
        pass

    def update_game_in_csv(self, game):
        """Update the corresponding row in the CSV file."""
        game_list = []
        try:
            with open(self.csv_path, "r", newline="\n") as file:
                reader = csv.reader(file)
                header = next(reader)
                for row in reader:
                    if row and row[0].isdigit():
                        current_game = Game(
                            id=int(row[0]),
                            title=row[1],
                            platform=row[2],
                            status=row[3],
                        )
                        current_game.rating = float(row[4]) if row[4] else None
                        current_game.review = row[5] if row[5] else None
                        current_game.date_added = datetime.strptime(row[6], "%Y-%m-%d").date() if row[6] else None
                        current_game.completion_date = datetime.strptime(row[7], "%Y-%m-%d").date() if row[7] else None
                        if current_game.id == game.id:
                            current_game = game
                    game_list.append(current_game.to_dict())

            with open(self.csv_path, "w", newline="\n") as file:
                writer = csv.DictWriter(file,
                                        fieldnames=["id", "title", "platform", "status", "rating", "review", "date_added",
                                                    "completion_date"])
                writer.writeheader()
                writer.writerows(game_list)
        except ValueError as e:
            print("Es ist ein Fehler aufgetreten")
            raise e


        # TODO: Add a try except block to handle the case where the file does not exist
        pass

    def add_game(self, title, platform, status="Want to Play"):
        """Add a new game to the library"""
        # TODO Add try/except block to handle duplicate games and raise a ValueError if it happens
        try:
            game = Game(
                id=self.next_id,
                title=title,
                platform=platform,
                status=status,
            )
            title2 = []
            for game2 in self.games:
                title2.append(game2.title)
            if game.title not in title2:
                self.save_to_csv(game)
                self.games.append(game)
                self.next_id += 1
                return game.to_dict()
            else:
                raise ValueError
        except ValueError as e:
            print("Es ist ein Fehler aufgetreten")
            raise e
    def update_game(self, game_id, status, rating=None, review=None):
        """Update an existing game's information"""
        for game in self.games:
            if game.id == game_id:  # Use object attribute
                game.update(status, rating, review)
                self.update_game_in_csv(game)
                return game.to_dict()
        return None

    def get_games(self, status=None):
        """Get games, optionally filtered by status"""
        if status and status != "All":
            filtered_games = [game for game in self.games if game.status == status]  # Use object attribute
        else:
            filtered_games = self.games
        return [game.to_dict() for game in filtered_games]

    def get_game_by_id(self, game_id):
        """Get a specific game by its ID"""
        #TODO: Add try/except block to handle the case where the game is not found
        for game in self.games:
            if game.id == game_id:  # Use object attribute
                return game.to_dict()
        return None