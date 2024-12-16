import tkinter as tk
from tkinter import messagebox
import random
import csv
import os

def ensure_csv_files_exist():
    """Ensure that the CSV files for categories exist."""
    categories = ['animals', 'things', 'plants']
    for category in categories:
        if not os.path.exists(f"{category}.csv"):
            with open(f"{category}.csv", mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Word"])

def read_category_from_csv(category):
    try:
        with open(f"{category}.csv", mode="r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            return [row[0] for row in reader]
    except FileNotFoundError:
        return []

def append_to_category_csv(category, words):
    with open(f"{category}.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        for word in words:
            writer.writerow([word])

class WordGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Adivinar Palabras Game")
        self.create_front_page()

    def create_front_page(self):
        """Create the front page of the game."""
        self.clear_window()

        title_label = tk.Label(self.root, text="Welcome to the Adivinar Palabras Game!", font=("Arial", 18))
        title_label.pack(pady=20)

        start_game_button = tk.Button(self.root, text="Start the Game", command=self.show_game_mode_selection, font=("Arial", 14))
        start_game_button.pack(pady=10)

        add_words_button = tk.Button(self.root, text="Add Words to Category", command=self.add_words_page, font=("Arial", 14))
        add_words_button.pack(pady=10)

        exit_button = tk.Button(self.root, text="Exit", command=self.root.quit, font=("Arial", 14), fg="red")
        exit_button.pack(pady=10)

    def add_words_page(self):
        """Page to add words to a category."""
        self.clear_window()

        label = tk.Label(self.root, text="Add Words to a Category", font=("Arial", 18))
        label.pack(pady=10)

        category_label = tk.Label(self.root, text="Select Category:", font=("Arial", 14))
        category_label.pack(pady=5)

        self.category_var = tk.StringVar(value="animals")
        category_menu = tk.OptionMenu(self.root, self.category_var, "animals", "things", "plants")
        category_menu.pack(pady=5)

        words_label = tk.Label(self.root, text="Enter words (comma-separated):", font=("Arial", 14))
        words_label.pack(pady=5)

        self.words_entry = tk.Entry(self.root, font=("Arial", 14), width=30)
        self.words_entry.pack(pady=5)

        save_button = tk.Button(self.root, text="Save", command=self.save_words, font=("Arial", 14))
        save_button.pack(pady=10)

        back_button = tk.Button(self.root, text="Back", command=self.create_front_page, font=("Arial", 14))
        back_button.pack(pady=10)

    def save_words(self):
        """Save words to the selected category."""
        category = self.category_var.get()
        words = self.words_entry.get().strip().split(",")
        words = [word.strip() for word in words if word.strip()]

        if not words:
            messagebox.showerror("Error", "Please enter at least one word.")
            return

        with open(f"{category}.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            for word in words:
                writer.writerow([word])

        messagebox.showinfo("Success", f"Added {len(words)} words to the {category} category.")
        self.words_entry.delete(0, tk.END)


    def show_game_mode_selection(self):
        """Show game mode selection dialog."""
        self.clear_window()

        mode_label = tk.Label(self.root, text="Select Game Mode", font=("Arial", 18))
        mode_label.pack(pady=20)

        solo_button = tk.Button(self.root, text="Solo Mode", command=self.start_solo_mode, font=("Arial", 14))
        solo_button.pack(side=tk.LEFT, padx=50, pady=20)

        multiplayer_button = tk.Button(self.root, text="Multiplayer Mode", command=self.start_multiplayer_mode, font=("Arial", 14))
        multiplayer_button.pack(side=tk.RIGHT, padx=50, pady=20)

    def start_solo_mode(self):
        """Start the main game in solo mode."""
        self.clear_window()
        game = MainGame(self.root)

    def start_multiplayer_mode(self):
        """Start multiplayer mode."""
        self.clear_window()
        multiplayer_game = MultiplayerGame(self.root)

    def clear_window(self):
        """Clears all widgets from the root window."""
        for widget in self.root.winfo_children():
            widget.destroy()

class MainGame:
    def __init__(self, root):
        self.root = root
        self.lives = 6
        self.remaining_hints = 1
        self.guessed_letters = []
        self.word = ""
        self.category = ""
        self.display = []

        ensure_csv_files_exist()
        self.setup_gui()

    def setup_gui(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20, padx=20)

        self.category_label = tk.Label(self.frame, text="Category: ", font=("Arial", 14))
        self.category_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.word_label = tk.Label(self.frame, text="Word: _ _ _", font=("Arial", 16))
        self.word_label.grid(row=1, column=0, columnspan=2, pady=10)

        self.lives_label = tk.Label(self.frame, text="Lives: 6", font=("Arial", 14))
        self.lives_label.grid(row=2, column=0, pady=10)

        self.hints_label = tk.Label(self.frame, text="Hints Remaining: 3", font=("Arial", 14))
        self.hints_label.grid(row=2, column=1, pady=10)

        self.guess_entry = tk.Entry(self.frame, font=("Arial", 14))
        self.guess_entry.grid(row=3, column=0, pady=10)

        self.guess_button = tk.Button(self.frame, text="Guess", command=self.make_guess, font=("Arial", 14))
        self.guess_button.grid(row=3, column=1, pady=10)

        self.hint_button = tk.Button(self.frame, text="Hint", command=self.use_hint, font=("Arial", 14))
        self.hint_button.grid(row=4, column=0, pady=10)

        self.back_button = tk.Button(self.frame, text="Back to Main Menu", command=self.go_back_to_main_menu, font=("Arial", 14))
        self.back_button.grid(row=4, column=1, pady=10)

        self.start_game_logic()

    def go_back_to_main_menu(self):
        """Return to the main menu."""
        self.frame.destroy()
        app.create_front_page()

    def start_game_logic(self):
        self.category = random.choice(["animals", "things", "plants"])
        self.word_list = read_category_from_csv(self.category)

        if not self.word_list:
            messagebox.showerror("Error", f"No words available in the '{self.category}' category. Add words to start.")
            return

        self.word = random.choice(self.word_list)
        self.display = ["_" for _ in self.word]

        self.lives = 6
        self.remaining_hints = 1
        self.guessed_letters = []

        self.update_status()

    def update_status(self):
        self.category_label.config(text=f"Category: {self.category.capitalize()}")
        self.word_label.config(text="Word: " + " ".join(self.display))
        self.lives_label.config(text=f"Lives: {self.lives}")
        self.hints_label.config(text=f"Hints Remaining: {self.remaining_hints}")

    def make_guess(self):
        guess = self.guess_entry.get().lower()
        self.guess_entry.delete(0, tk.END)

        if not guess or len(guess) != 1 or not guess.isalpha():
            messagebox.showerror("Error", "Please enter a valid single letter.")
            return

        if guess in self.guessed_letters:
            messagebox.showwarning("Warning", "You already guessed that letter.")
            return

        self.guessed_letters.append(guess)

        if guess in self.word:
            for i, letter in enumerate(self.word):
                if letter == guess:
                    self.display[i] = guess
        else:
            self.lives -= 1

        if "_" not in self.display:
            messagebox.showinfo("Congratulations!", f"You guessed the word '{self.word}'!")
            self.start_game_logic()
        elif self.lives == 0:
            messagebox.showinfo("Game Over", f"You ran out of lives. The word was '{self.word}'.")
            self.start_game_logic()
        else:
            self.update_status()

    def use_hint(self):
        if self.remaining_hints > 0:
            hint = random.choice([letter for letter in self.word if letter not in self.guessed_letters])
            self.remaining_hints -= 1
            messagebox.showinfo("Hint", f"One of the letters is '{hint}'")
        else:
            messagebox.showwarning("No Hints Left", "You have no more hints remaining.")
        
        self.update_status()

class MultiplayerGame:
    def __init__(self, root):
        self.root = root
        self.player_turn = 0  # 0 for Player 1, 1 for Player 2
        self.players = ["Player 1", "Player 2"]
        self.lives = [6, 6]  # Lives per player
        self.hints = [2, 2]  # Hints per player in multiplayer mode
        self.guessed_letters = []
        self.word = ""
        self.category = ""
        self.display = []

        ensure_csv_files_exist()
        self.setup_gui()
        self.start_game_logic()

    def setup_gui(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20, padx=20)

        self.player_label = tk.Label(self.frame, text="Player: Player 1", font=("Arial", 14))
        self.player_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.category_label = tk.Label(self.frame, text="Category: ", font=("Arial", 14))
        self.category_label.grid(row=1, column=0, columnspan=2, pady=10)

        self.word_label = tk.Label(self.frame, text="Word: _ _ _", font=("Arial", 16))
        self.word_label.grid(row=2, column=0, columnspan=2, pady=10)

        self.lives_label = tk.Label(self.frame, text="Lives: Player 1 - 6 | Player 2 - 6", font=("Arial", 14))
        self.lives_label.grid(row=3, column=0, columnspan=2, pady=10)

        self.hints_label = tk.Label(self.frame, text="Hints: Player 1 - 2 | Player 2 - 2", font=("Arial", 14))
        self.hints_label.grid(row=4, column=0, columnspan=2, pady=10)

        self.guess_entry = tk.Entry(self.frame, font=("Arial", 14))
        self.guess_entry.grid(row=5, column=0, pady=10)

        self.guess_button = tk.Button(self.frame, text="Guess", command=self.make_guess, font=("Arial", 14))
        self.guess_button.grid(row=5, column=1, pady=10)

        self.hint_button = tk.Button(self.frame, text="Hint", command=self.use_hint, font=("Arial", 14))
        self.hint_button.grid(row=6, column=0, pady=10)

        self.back_button = tk.Button(self.frame, text="Back to Main Menu", command=self.go_back_to_main_menu, font=("Arial", 14))
        self.back_button.grid(row=6, column=1, pady=10)

    def go_back_to_main_menu(self):
        """Return to the main menu."""
        self.frame.destroy()
        app.create_front_page()

    def start_game_logic(self):
        self.category = random.choice(["animals", "things", "plants"])
        self.word_list = read_category_from_csv(self.category)

        if not self.word_list:
            messagebox.showerror("Error", f"No words available in the '{self.category}' category. Add words to start.")
            return

        self.word = random.choice(self.word_list)
        self.display = ["_" for _ in self.word]

        self.lives = [6, 6]
        self.hints = [2, 2]  # Reset hints for both players
        self.guessed_letters = []

        self.update_status()

    def update_status(self):
        self.player_label.config(text=f"Player: {self.players[self.player_turn]}")
        self.category_label.config(text=f"Category: {self.category.capitalize()}")
        self.word_label.config(text="Word: " + " ".join(self.display))
        self.lives_label.config(text=f"Lives: Player 1 - {self.lives[0]} | Player 2 - {self.lives[1]}")
        self.hints_label.config(text=f"Hints: Player 1 - {self.hints[0]} | Player 2 - {self.hints[1]}")

    def make_guess(self):
        guess = self.guess_entry.get().lower()
        self.guess_entry.delete(0, tk.END)

        if not guess or len(guess) != 1 or not guess.isalpha():
            messagebox.showerror("Error", "Please enter a valid single letter.")
            return

        if guess in self.guessed_letters:
            messagebox.showwarning("Warning", "You already guessed that letter.")
            return

        self.guessed_letters.append(guess)

        if guess in self.word:
            for i, letter in enumerate(self.word):
                if letter == guess:
                    self.display[i] = guess

            if "_" not in self.display:
                messagebox.showinfo("Congratulations!", f"{self.players[self.player_turn]} guessed the word '{self.word}'!")
                self.start_game_logic()
            else:
                self.update_status()
        else:
            self.lives[self.player_turn] -= 1
            if self.lives[self.player_turn] == 0:
                messagebox.showinfo("Game Over", f"{self.players[self.player_turn]} lost all lives. The word was '{self.word}'.")
                self.start_game_logic()
            else:
                self.player_turn = (self.player_turn + 1) % len(self.players)
                self.update_status()

    def use_hint(self):
        if self.hints[self.player_turn] > 0:
            hint = random.choice([letter for letter in self.word if letter not in self.guessed_letters])
            self.hints[self.player_turn] -= 1
            messagebox.showinfo("Hint", f"One of the letters is '{hint}'")
        else:
            messagebox.showwarning("No Hints Left", f"{self.players[self.player_turn]} has no hints remaining.")

        self.update_status()

    def switch_turn(self):
        """Switch turns between players."""
        self.player_turn = (self.player_turn + 1) % len(self.players)
        self.update_status()

if __name__ == "__main__":
    root = tk.Tk()
    app = WordGameGUI(root)
    root.mainloop()