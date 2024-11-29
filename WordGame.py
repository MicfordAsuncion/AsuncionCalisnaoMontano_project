import random

def select_random_category():
    """
    Randomly selects a category from the available ones.
    """
    categories = ['animals', 'things', 'plants']
    category = random.choice(categories)
    print(f"Randomly selected category: {category}")
    return category

def select_word_list(category):
    """
    Returns a word list based on the chosen category.
    """
    animals = ["cat", "dog", "bird", "fish", "lion", "tiger", "elephant", "zebra"]
    things = ["computer", "phone", "desk", "lamp", "key", "bottle", "window", "chair"]
    plants = ["rose", "daisy", "sunflower", "oak", "maple", "cactus", "bamboo", "fern"]
    
    if category == "animals":
        return animals
    elif category == "things":
        return things
    elif category == "plants":
        return plants

def give_category_hint(category):
    """
    Gives a hint based on the selected category.
    """
    if category == "animals":
        return "It is a living creature."
    elif category == "things":
        return "It is an object you can touch or use."
    elif category == "plants":
        return "It is a type of plant that grows in nature."

def give_one_letter_hint(word, guessed_letters):
    """
    Provides a single letter hint by revealing one of the letters that hasn't been guessed yet.
    """
    remaining_letters = [letter for letter in word if letter not in guessed_letters]
    if remaining_letters:
        hint = random.choice(remaining_letters)
        print(f"Hint: One of the remaining letters is '{hint}'")
        return hint
    else:
        print("No hints available.")
        return None

def display_status(display, lives, remaining_hints):
    """
    Displays the current status of the game, including the word's progress, remaining lives, and hints left.
    """
    print("\n" + " ".join(display))
    print(f"Lives left: {lives}")
    print(f"Remaining hints: {remaining_hints}")

def wordgame():
    """
    The main hangman word game function, with random categories and hints.
    """
    print("Welcome to the Adivinar Palabras Game!")

    # Ask the user for play mode
    play_mode = input("Do you want to play solo or team? (solo/team): ").lower()
    
    while play_mode not in ['solo', 'team']:
        play_mode = input("Invalid choice. Do you want to play solo or team? (solo/team): ").lower()
    
    # Choose the number of players for team mode
    if play_mode == 'team':
        num_players = int(input("How many players are in your team? (2 or 3): "))
        while num_players not in [2, 3]:
            num_players = int(input("Invalid choice. How many players are in your team? (2 or 3): "))
    else:
        num_players = 1  # Solo game

    # Randomly choose a category
    category = select_random_category()

    # Select the word list based on category
    word_list = select_word_list(category)

    # Choose a random word from the selected list
    word = random.choice(word_list)

    # Give a hint related to the selected category
    category_hint = give_category_hint(category)
    print(f"\nCategory hint: {category_hint}")

    # Ask user to choose difficulty
    difficulty = input("Choose difficulty (easy/normal/expert): ").lower()
    while difficulty not in ["easy", "normal", "expert"]:
        difficulty = input("Invalid choice. Please choose 'easy', 'normal', or 'expert': ").lower()

    # Set the initial number of lives based on difficulty
    lives = {"easy": 8, "normal": 6, "expert": 4}[difficulty]

    # Initialize player scores
    players_scores = {f"Player {i+1}": 0 for i in range(num_players)}
    
    # Word progress and guessed letters
    display = ["_"] * len(word)
    guessed_letters = []
    
    current_player = 0  # For solo or team play, we cycle through players if it's team play
    
    remaining_hints = 3  # Players are allowed up to 3 hints

    while lives > 0:
        # Display game status
        print(f"\nIt's {f'Player {current_player + 1}'}'s turn:")
        display_status(display, lives, remaining_hints)

        # Ask if the player wants a hint
        if remaining_hints > 0:
            get_hint = input("Do you want a hint? (yes/no): ").lower()
            while get_hint not in ['yes', 'no']:
                get_hint = input("Invalid input. Do you want a hint? (yes/no): ").lower()

            # If the player wants a hint
            if get_hint == "yes":
                remaining_hints -= 1  # Decrease the remaining hints
                give_one_letter_hint(word, guessed_letters)  # Provide a hint
            else:
                print("No hint provided.")
        else:
            print("You have no hints left.")

        # Ask for a letter guess
        guess = input("Guess a letter: ").lower()

        # Validate the guess
        if guess in guessed_letters:
            print("You already guessed that letter. Try again.")
        elif len(guess) != 1 or not guess.isalpha():
            print("Invalid input. Please enter a single letter.")
        else:
            guessed_letters.append(guess)
            if guess in word:
                print("Good job!")
                for i in range(len(word)):
                    if word[i] == guess:
                        display[i] = guess
                players_scores[f"Player {current_player + 1}"] += 1  # Increase score for correct guess
            else:
                lives -= 1
                print(f"Incorrect guess. You lost a life.")

        # Check if the word is fully guessed
        if "_" not in display:
            print(f"\nCongratulations! {f'Player {current_player + 1}'} solved the word '{word}'!")
            break

        # Check if out of lives
        if lives == 0:
            print(f"\nGame over! The word was: {word}")
            break

        # Switch to the next player
        current_player = (current_player + 1) % num_players

    # Final score display for competitive mode
    print("\nGame Over!")
    print("Final scores:")
    for player, player_score in players_scores.items():
        print(f"{player}: {player_score} points")
    
    # Determine and display the winner or tie
    if num_players > 1:  # Only in team mode
        max_score = max(players_scores.values())
        winners = [player for player, score in players_scores.items() if score == max_score]

        if len(winners) > 1:
            print("\nIt's a tie between:", ", ".join(winners))
        else:
            print(f"\n{winners[0]} wins the game!")
    
    # Ask the user if they want to play again
    play_again = input("Do you want to play again? (yes/no): ").lower()
    if play_again == 'yes':
        wordgame()  # Restart the game if the player says 'yes'
    else:
        print("Thanks for playing Adivinar Palabras!! See you again Goodbye!")

# Start the game
wordgame()