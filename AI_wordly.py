import random
from termcolor import colored, cprint
from transformers import pipeline
import nltk
import requests
from pyfiglet import figlet_format

# Load a multilingual model for broader language support
model_name = "bigscience/bloom-560m"  # BLOOM is multilingual and better for non-English words
text_gen = pipeline("text-generation", model=model_name)

# Language dictionary for prompts
language_prompts = {
    "en": "Give me a five-letter English word:",
    "es": "Dame una palabra en español de cinco letras:",
    "fr": "Donne-moi un mot français de cinq lettres:",
    "de": "Gib mir ein deutsches Wort mit fünf Buchstaben:",
    "it": "Dammi una parola italiana di cinque lettere:",
    "ru": "Дай мне русское слово из пяти букв:"  # Russian prompt
}

# UI translations
ui_text = {
    "en": {
        "welcome": "Welcome to the Multilingual Word Guessing Game!",
        "menu_play_ai": "1. Play with AI",
        "menu_play_friends": "2. Play with Friends",
        "menu_difficulty": "3. Play with Difficulty Settings",
        "choose_option": "Choose an option (1-3):",
        "choose_difficulty": "Choose difficulty: 1 (Easy), 2 (Medium), 3 (Hard), 4 (Extreme)",
        "enter_difficulty": "Enter difficulty:",
        "invalid_choice": "Invalid choice.",
        "select_language": "Select a language:",
        "guess_prompt": "Enter your 5-letter guess (or type 'hint'):",
        "hint_text": "Hint: The word contains the letter",
        "correct": "You guessed it in {attempts} attempts!",
        "out_of_attempts": "Out of attempts! The word was:"
    },
    "ru": {
        "welcome": "Добро пожаловать в многоязычную игру угадай слово!",
        "menu_play_ai": "1. Играть с ИИ",
        "menu_play_friends": "2. Играть с другом",
        "menu_difficulty": "3. Сложность",
        "choose_option": "Выберите опцию (1-3):",
        "choose_difficulty": "Выберите сложность: 1 (Легко), 2 (Средне), 3 (Сложно), 4 (Экстрим)",
        "enter_difficulty": "Введите уровень сложности:",
        "invalid_choice": "Неверный выбор.",
        "select_language": "Выберите язык:",
        "guess_prompt": "Введите слово из 5 букв (или 'hint' для подсказки):",
        "hint_text": "Подсказка: слово содержит букву",
        "correct": "Вы угадали за {attempts} попыток!",
        "out_of_attempts": "Попытки закончились! Загаданное слово было:"
    }
}

# Function to select a language
def select_language():
    print(ui_text["en"]["select_language"])
    for idx, lang in enumerate(language_prompts.keys()):
        print(f"{idx + 1}. {lang}")
    choice = int(input("Enter choice: "))
    lang_code = list(language_prompts.keys())[choice - 1]
    return lang_code

# Function to validate word using NLTK (for English) or API for other languages
def is_valid_word(word, language="en"):
    if language == "en":
        nltk.download('words')
        from nltk.corpus import words
        return word in words.words()
    else:
        if language == "ru":
            url = f"https://api.dictionaryapi.dev/api/v2/entries/ru/{word}"
            response = requests.get(url)
            return response.status_code == 200
        return True

# Function to generate a 5-letter word using multilingual AI
def generate_ai_word(lang="en"):
    prompt = language_prompts.get(lang, language_prompts["en"])
    while True:
        output = text_gen(prompt, max_length=15, num_return_sequences=1, do_sample=True, temperature=0.9)[0]['generated_text']
        words = output.split()
        for word in words:
            if word.isalpha() and len(word) == 5:
                if is_valid_word(word.lower(), lang):
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
def play_wordly(mode="ai", difficulty=1, language="en"):
    if mode == "friends":
        target_word = input("Player 1, enter your secret 5-letter word: ").lower()
        print("\n" * 50)
    else:
        target_word = generate_ai_word(lang=language)

    max_attempts = {1: float('inf'), 2: 10, 3: 5, 4: 3}[difficulty]
    hints = {1: 3, 2: 1, 3: 0, 4: 0}[difficulty]

    print(f"\n{ui_text[language]['welcome']}")
    print(f"{max_attempts if max_attempts != float('inf') else '∞'} попыток!")

    attempts = 0
    used_hints = 0

    while attempts < max_attempts:
        guess = input(ui_text[language]["guess_prompt"]).lower()
        if guess == "hint" and used_hints < hints:
            print(f"{ui_text[language]['hint_text']} '{random.choice(target_word)}'")
            used_hints += 1
            continue

        if len(guess) != 5 or not guess.isalpha():
            print("Введите корректное слово из 5 букв.")
            continue

        attempts += 1
        display_feedback(guess, target_word)

        if guess == target_word:
            print(ui_text[language]["correct"].format(attempts=attempts))
            return

    print(f"{ui_text[language]['out_of_attempts']} {target_word}")

# Banner with language support
def print_banner(language="en"):
    banner = figlet_format("AI Wordly", font="slant")
    cprint(banner, "cyan")
    print("=" * 60)
    cprint(ui_text[language]["welcome"], "green", attrs=["bold"])
    print("=" * 60)

# Main menu with translated UI
def main_menu():
    language = select_language()
    print_banner(language)
    cprint(ui_text[language]["menu_play_ai"], "yellow")
    cprint(ui_text[language]["menu_play_friends"], "yellow")
    cprint(ui_text[language]["menu_difficulty"], "yellow")
    print()

    choice = input(ui_text[language]["choose_option"])

    if choice == "1":
        play_wordly(mode="ai", language=language)
    elif choice == "2":
        play_wordly(mode="friends", language=language)
    elif choice == "3":
        cprint(ui_text[language]["choose_difficulty"], "magenta")
        diff = int(input(ui_text[language]["enter_difficulty"]))
        play_wordly(mode="ai", difficulty=diff, language=language)
    else:
        cprint(ui_text[language]["invalid_choice"], "red")

if name == '__main__':
    main_menu()
