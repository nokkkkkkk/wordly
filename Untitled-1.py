import random
from termcolor import colored
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "gpt2" 
text_gen = pipeline("text-generation", model=model_name)

# Языковой словарь для подсказок
language_prompts = {
    "en": "Give me a five-letter word:",
    "es": "Dame una palabra de cinco letras:",
    "fr": "Donne-moi un mot de cinq lettres:",
    "de": "Gib mir ein fünf Buchstaben langes Wort:",
    "it": "Dammi una parola di cinque lettere:",
    "ru": "Дай мне слово из пяти букв:",
}

# Функция выбора языка
def select_language():
    print("Select a language:")
    for idx, lang in enumerate(language_prompts.keys()):
        print(f"{idx + 1}. {lang}")
    choice = int(input("Enter choice: "))
    lang_code = list(language_prompts.keys())[choice - 1]
    return lang_code

# Функция для генерации слова из 5 букв
def generate_ai_word(lang="en"):
    prompt = language_prompts.get(lang, language_prompts["en"])
    while True:
        output = text_gen(prompt, max_length=15, num_return_sequences=1)[0]['generated_text']
        words = output.split()
        for word in words:
            if word.isalpha() and len(word) == 5:
                return word.lower()

# Функция отображения слова с цветовой обратной связью
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

# Основная игровая функция
def play_wordly(mode="ai", difficulty=1, language="en"):
    if mode == "friends":
        target_word = input("Player 1, enter your secret 5-letter word: ").lower()
        print("\n" * 50)  # Очистить экран
    else:
        target_word = generate_ai_word(lang=language)

    max_attempts = {1: float('inf'), 2: 10, 3: 5, 4: 3}[difficulty]
    hints = {1: 3, 2: 1, 3: 0, 4: 0}[difficulty]

    print(f"\nWelcome to Wordly! You have {max_attempts if max_attempts != float('inf') else 'infinite'} attempts!")

    attempts = 0
    used_hints = 0

    while attempts < max_attempts:
        guess = input("Enter your 5-letter guess (or type 'hint'): ").lower()
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

# Система меню
def main_menu():
    print("Welcome to AI Wordly!")
    print("1. Play with AI")
    print("2. Play with Friends")
    print("3. Play with Difficulty Settings")

    choice = input("Choose an option (1-3): ")
    language = select_language()

    if choice == "1":
        play_wordly(mode="ai", language=language)
    elif choice == "2":
        play_wordly(mode="friends", language=language)
    elif choice == "3":
        print("Choose difficulty: 1 (Easy), 2 (Medium), 3 (Hard), 4 (Extreme)")
        diff = int(input("Enter difficulty: "))
        play_wordly(mode="ai", difficulty=diff, language=language)
    else:
        print("Invalid choice.")

if name == '__main__':
    main_menu()
