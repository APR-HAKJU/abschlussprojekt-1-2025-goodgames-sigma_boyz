import tkinter as tk
from tkinter import ttk, messagebox
from backend import GameLibrary
import csv


class GoodGamesApp:
    """Main application class for GoodGames"""

    def __init__(self, root):
        """Initialize the main application window and setup UI"""
        self.root = root
        self.root.title("GoodGames - Game Collection Tracker")

        # Initialize game library
        self.library = GameLibrary()

        # Setup main container
        self.setup_main_container()

        # Create tabs
        self.create_notebook()

        # Setup individual tabs
        self.setup_add_game_tab()
        self.setup_library_tab()

        # Bind tab change event
        self.notebook.bind("<<NotebookTabChanged>>", lambda e: self.refresh_library())

    def setup_main_container(self):
        """Setup the main container frame"""
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    def create_notebook(self):
        """Create the notebook (tabbed interface)"""
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create frames for each tab
        self.add_game_frame = ttk.Frame(self.notebook)
        self.library_frame = ttk.Frame(self.notebook)

        # Add frames to notebook
        self.notebook.add(self.add_game_frame, text="Add New Game")
        self.notebook.add(self.library_frame, text="Game Library")

    def setup_add_game_tab(self):
        """Setup the Add Game tab interface"""
        # Game Title
        ttk.Label(self.add_game_frame, text="Game Title:").grid(row=0, column=0, pady=5)
        self.title_var = tk.StringVar()
        ttk.Entry(
            self.add_game_frame,
            textvariable=self.title_var,
            width=40
        ).grid(row=0, column=1, pady=5)

        # Platform
        ttk.Label(self.add_game_frame, text="Platform:").grid(row=1, column=0, pady=5)
        self.platform_var = tk.StringVar()
        ttk.Entry(
            self.add_game_frame,
            textvariable=self.platform_var,
            width=40
        ).grid(row=1, column=1, pady=5)

        # Status
        ttk.Label(self.add_game_frame, text="Status:").grid(row=2, column=0, pady=5)
        self.status_var = tk.StringVar(value="Want to Play")
        status_combo = ttk.Combobox(
            self.add_game_frame,
            textvariable=self.status_var,
            width=37,
            values=("Want to Play", "Playing", "Completed", "Abandoned")
        )
        status_combo.grid(row=2, column=1, pady=5)

        # Add Button
        ttk.Button(
            self.add_game_frame,
            text="Add Game to Library",
            command=self.add_game
        ).grid(row=3, column=0, columnspan=2, pady=20)

    def setup_library_tab(self):
        """Setup the Library tab interface"""
        # Create left and right frames for split layout
        left_frame = ttk.Frame(self.library_frame)
        left_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        right_frame = ttk.Frame(self.library_frame)
        right_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # Configure grid weights
        self.library_frame.grid_columnconfigure(0, weight=3)
        self.library_frame.grid_columnconfigure(1, weight=2)

        # Setup components
        self.setup_library_filter(left_frame)
        self.setup_library_treeview(left_frame)
        self.setup_game_details(left_frame)
        self.setup_game_overview(right_frame)

        self.refresh_library()

    def setup_library_filter(self, parent):
        """Setup the status filter in the library tab"""
        ttk.Label(parent, text="Filter by Status:").grid(row=0, column=0, pady=5)

        self.filter_var = tk.StringVar(value="All")
        filter_combo = ttk.Combobox(
            parent,
            textvariable=self.filter_var,
            width=37,
            values=("All", "Want to Play", "Playing", "Completed", "Abandoned")
        )
        filter_combo.grid(row=0, column=1, pady=5)
        filter_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_library())

    def setup_library_treeview(self, parent):
        """Setup the treeview that displays the game library"""
        # Create Treeview
        self.tree = ttk.Treeview(
            parent,
            columns=("ID", "Title", "Platform", "Status", "Rating"),
            show="headings"
        )
        self.tree.grid(row=1, column=0, columnspan=2, pady=10)

        # Configure columns
        columns = {
            "ID": 50,
            "Title": 200,
            "Platform": 100,
            "Status": 100,
            "Rating": 50
        }

        for col, width in columns.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            self.library_frame,
            orient=tk.VERTICAL,
            command=self.tree.yview
        )
        scrollbar.grid(row=1, column=2, sticky='ns')
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def setup_game_details(self, parent):
        """Setup the game details section"""
        details_frame = ttk.LabelFrame(parent, text="Game Details", padding="10")
        details_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky='ew')

        # Rating
        ttk.Label(details_frame, text="Rating (1-5):").grid(row=0, column=0, pady=5)
        self.rating_var = tk.StringVar()
        rating_spin = ttk.Spinbox(
            details_frame,
            from_=1,
            to=5,
            textvariable=self.rating_var,
            width=5
        )
        rating_spin.grid(row=0, column=1, pady=5)

        # Review
        ttk.Label(details_frame, text="Review:").grid(row=1, column=0, pady=5)
        self.review_text = tk.Text(details_frame, height=4, width=40)
        self.review_text.grid(row=1, column=1, pady=5)

        # Update button
        ttk.Button(
            details_frame,
            text="Update Game Details",
            command=self.update_game
        ).grid(row=2, column=0, columnspan=2, pady=10)

    def setup_game_overview(self, parent):
        """Setup the game overview panel"""
        overview_frame = ttk.LabelFrame(parent, text="Game Overview", padding="10")
        overview_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # Setup overview labels
        self.setup_overview_labels(overview_frame)

        # Configure grid
        overview_frame.grid_columnconfigure(1, weight=1)

    def setup_overview_labels(self, frame):
        """Setup all labels in the overview panel"""
        labels = [
            ("Title:", "overview_title"),
            ("Platform:", "overview_platform"),
            ("Status:", "overview_status"),
            ("Rating:", "overview_rating"),
            ("Added On:", "overview_date_added"),
            ("Completed On:", "overview_completion_date")
        ]

        for i, (text, attr_name) in enumerate(labels):
            ttk.Label(frame, text=text, font=("", 10, "bold")).grid(
                row=i, column=0, sticky="w", pady=5
            )
            setattr(self, attr_name, ttk.Label(frame, text=""))
            getattr(self, attr_name).grid(row=i, column=1, sticky="w", pady=5)

        # Review section
        ttk.Label(frame, text="Review:", font=("", 10, "bold")).grid(
            row=len(labels), column=0, sticky="w", pady=5
        )
        self.overview_review = tk.Text(frame, height=8, width=35, wrap=tk.WORD)
        self.overview_review.grid(row=len(labels), column=1, sticky="w", pady=5)
        self.overview_review.configure(state='disabled')

    # Event Handlers
    def add_game(self):
        """Handle adding a new game"""
        title = self.title_var.get().strip()
        platform = self.platform_var.get().strip()
        status = self.status_var.get()

        if not title or not platform:
            messagebox.showerror("Error", "Title and Platform are required!")
            return

        self.library.add_game(title, platform, status)

        # Clear inputs
        self.title_var.set("")
        self.platform_var.set("")
        self.status_var.set("Want to Play")

        # Show success message
        messagebox.showinfo("Success", "Game added successfully!")

        # Refresh library view
        self.refresh_library()

    def update_game(self):
        """Handle updating game details"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showerror("Error", "Please select a game to update!")
            return

        game_id = self.tree.item(selection[0])['values'][0]
        status = self.tree.item(selection[0])['values'][3]
        rating = self.rating_var.get()
        review = self.review_text.get("1.0", tk.END).strip()

        # Convert rating to integer or None
        try:
            rating = int(rating) if rating else None
        except ValueError:
            messagebox.showerror("Error", "Rating must be a number between 1 and 5!")
            return

        # Update game
        self.library.update_game(game_id, status, rating, review)

        # Refresh views
        self.refresh_library()
        self.on_select()  # Refresh details view
        messagebox.showinfo("Success", "Game updated successfully!")

    def refresh_library(self):
        """Refresh the library view"""
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Get filtered games
        games = self.library.get_games(self.filter_var.get())

        # Add games to treeview
        for game in games:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    game['id'],
                    game['title'],
                    game['platform'],
                    game['status'],
                    game['rating'] if game['rating'] else ""
                )
            )

    def on_select(self, event=None):
        """Handle game selection in library"""
        selection = self.tree.selection()
        if not selection:
            return

        # Clear previous values
        self.clear_details()

        # Get selected game
        game_id = self.tree.item(selection[0])['values'][0]
        game = self.library.get_game_by_id(game_id)

        if game:
            self.update_details_view(game)
            self.update_overview_panel(game)

    def clear_details(self):
        """Clear all detail fields"""
        self.rating_var.set("")
        self.review_text.delete("1.0", tk.END)
        self.overview_review.configure(state='normal')
        self.overview_review.delete("1.0", tk.END)
        self.overview_review.configure(state='disabled')

    def update_details_view(self, game):
        """Update the details view with game data"""
        if game['rating']:
            self.rating_var.set(str(game['rating']))
        if game['review']:
            self.review_text.insert("1.0", game['review'])

    def update_overview_panel(self, game):
        """Update the overview panel with the selected game's data"""
        # Basic info with fallbacks
        self.overview_title.config(text=game.get('title', 'No title'))
        self.overview_platform.config(text=game.get('platform', 'No platform'))
        self.overview_status.config(text=game.get('status', 'Unknown'))
        self.overview_rating.config(text=str(game.get('rating')) if game.get('rating') else "Not rated")

        # Date handling
        date_added = game.get('date_added')
        completion_date = game.get('completion_date')  # Note: matches backend field name

        self.overview_date_added.config(
            text=date_added.strftime("%Y-%m-%d") if date_added else "No date recorded"
        )

        self.overview_completion_date.config(
            text=completion_date.strftime("%Y-%m-%d") if completion_date else "Not completed"
        )

        # Review handling
        self.overview_review.configure(state='normal')
        self.overview_review.delete("1.0", tk.END)

        review_text = game.get('review', 'No review yet')
        self.overview_review.insert("1.0", review_text)
        self.overview_review.configure(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = GoodGamesApp(root)
    root.mainloop()