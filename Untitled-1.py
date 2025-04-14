import random
from termcolor import colored # type: ignore
from transformers import pipeline

# Load a multilingual model to generate words (AI-powered)
text_gen = pipeline("text-generation", model="gpt2")  # Replace with multilingual GPT if needed

# Function to generate a 5-letter word (basic simulation)
def generate_ai_word():
    while True:
        output = text_gen("Give me a five-letter word:", max_length=10, num_return_sequences=1)[0]['generated_text']
        words = output.split()
        for word in words:
            if word.isalpha() and len(word) == 5:
                return word.lower()

# Function to display word with color-coded feedback
def display_feedback(guess, target):
    result = ""
    for i in range(5):
        if guess[i] == target[i]:
            result += colored(guess[i], "green")
        elif guess[i] in target:
            result += colored(guess[i], "yellow")
        else:
            result += colored(guess[i], "white")
    print(result)

# Main game function
def play_wordly(mode="ai", difficulty=1):
    if mode == "friends":
        target_word = input("Player 1, enter your secret 5-letter word: ").lower()
        print("\n" * 50)  # Clear screen
    else:
        target_word = generate_ai_word()

    max_attempts = {1: float('inf'), 2: 10, 3: 5, 4: 3}[difficulty]
    hints = {1: 3, 2: 1, 3: 0, 4: 0}[difficulty]

    print(f"\nWelcome to Wordly! You have {max_attempts if max_attempts != float('inf') else 'infinite'} attempts!")

    attempts = 0
    used_hints = 0

    while attempts < max_attempts:
        guess = input("Enter your 5-letter guess: ").lower()
        if guess == "hint" and used_hints < hints:
            print(f"Hint: The word contains the letter '{random.choice(target_word)}'")
            used_hints += 1
            continue

        if len(guess) != 5 or not guess.isalpha():
            print("Please enter a valid 5-letter word.")
            continue

        attempts += 1
        display_feedback(guess, target_word)

        if guess == target_word:
            print(f"You guessed it in {attempts} attempts!")
            return

    print(f"Out of attempts! The word was: {target_word}")

# Menu system
def main_menu():
    print("Welcome to AI Wordly!")
    print("1. Play with AI")
    print("2. Play with Friends")
    print("3. Difficulty Settings")
    choice = input("Choose an option (1-3): ")

    if choice == "1":
        play_wordly(mode="ai")
    elif choice == "2":
        play_wordly(mode="friends")
    elif choice == "3":
        print("Choose difficulty: 1 (Easy), 2 (Medium), 3 (Hard), 4 (Extreme)")
        diff = int(input("Enter difficulty: "))
        play_wordly(mode="ai", difficulty=diff)
    else:
        print("Invalid choice.")