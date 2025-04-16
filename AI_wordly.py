from transformers import pipeline, AutoTokenizer, AutoModelWithLMHead
from termcolor import colored
import random
import sys
import pymorphy2
from langdetect import detect

# Загрузка морфологический анализатор для проверки существительных
morph = pymorphy2.MorphAnalyzer()

# Загрузка GPT-модель
print("Загрузка ИИ...")
try:
    tokenizer = AutoTokenizer.from_pretrained("sberbank-ai/rugpt3small_based_on_gpt2")
    model = AutoModelWithLMHead.from_pretrained("sberbank-ai/rugpt3small_based_on_gpt2")
    text_gen = pipeline("text-generation", model=model, tokenizer=tokenizer)
except Exception as e:
    print("Ошибка загрузки модели RuGPT:", e)
    text_gen = None

# Запасной список слов
fallback_words = ["лампа", "песня", "завод", "носик", "снега", "чайка", "город", "листь", "водач", "время"]

# Проверка, является ли слово русским существительным
def is_russian_noun(word):
    if detect(word) != "ru":
        return False
    parsed = morph.parse(word)
    return any(p.tag.POS == 'NOUN' for p in parsed)

# Генерация на основе искусственного интеллекта 5-буквенное русское существительное
def generate_word():
    if text_gen:
        prompt = "Придумай одно существительное на русском языке, состоящее из 5 букв:"
        try:
            for _ in range(5):  
                response = text_gen(prompt, max_length=20, num_return_sequences=1)
                word = response[0]['generated_text'].strip().split()[-1]
                word = ''.join(filter(str.isalpha, word)).lower()
                if len(word) == 5 and is_russian_noun(word):
                    return word
        except Exception as e:
            print("Ошибка генерации:", e)
    return random.choice(fallback_words)

# Оценка в стиле Wordle
def evaluate_guess(secret_word, guess):
    output = ""
    for i in range(5):
        if guess[i] == secret_word[i]:
            output += colored(guess[i], "green")
        elif guess[i] in secret_word:
            output += colored(guess[i], "yellow")
        else:
            output += guess[i]
    print(output)

# Уровни сложности
difficulties = {
    "1": {"tries": 1000, "hints": 3, "name": "Лёгкий (бесконечные попытки, 3 подсказки)"},
    "2": {"tries": 10, "hints": 1, "name": "Средний (10 попыток, 1 подсказка)"},
    "3": {"tries": 5, "hints": 0, "name": "Сложный (5 попыток, без подсказок)"},
    "4": {"tries": 3, "hints": 0, "name": "Хардкор (3 попытки, без подсказок)"},
}

# Режим искусственного интеллекта
def play_with_ai():
    print("\nВыберите уровень сложности:")
    for key in difficulties:
        print(f"{key}. {difficulties[key]['name']}")
    choice = input("Ваш выбор: ")
    level = difficulties.get(choice, difficulties["1"])
    
    secret = generate_word()
    attempts = level["tries"]
    hints = level["hints"]
    
    print("\nУгадай существительное из 5 букв. Введи 'hint' для подсказки.\n")

    while attempts > 0:
        guess = input("Введите слово: ").strip().lower()
        if guess == "hint" and hints > 0:
            print(colored(f"Подсказка: первая буква — {secret[0]}", "cyan"))
            hints -= 1
            continue
        if len(guess) != 5:
            print("Слово должно быть из 5 букв.")
            continue
        evaluate_guess(secret, guess)
        if guess == secret:
            print(colored("Поздравляем! Вы угадали слово!", "green"))
            return
        attempts -= 1
        print(f"Осталось попыток: {attempts}, подсказок: {hints}")
    
    print(colored(f"Вы проиграли. Загаданное слово было: {secret}", "red"))

# Многопользовательский режим
def play_with_friend():
    print("\nИгрок 1, введите слово из 5 букв:")
    secret = input("Секретное слово: ").strip().lower()
    print("\n" * 50)  # Очистить экран
    print("Игрок 2, угадывай слово!")

    attempts = 6
    while attempts > 0:
        guess = input("Ваше предположение: ").strip().lower()
        if len(guess) != 5:
            print("Слово должно быть из 5 букв.")
            continue
        evaluate_guess(secret, guess)
        if guess == secret:
            print(colored("Угадано! Победа!", "green"))
            return
        attempts -= 1
        print(f"Осталось попыток: {attempts}")
    print(colored(f"Увы! Слово было: {secret}", "red"))

# Баннер
def show_banner():
    print(colored("\n" + "="*30, "magenta"))
    print(colored("     Добро пожаловать в Wordly!", "magenta"))
    print(colored("     Игра на угадывание слов", "cyan"))
    print(colored("="*30 + "\n", "magenta"))

# Меню
def main():
    show_banner()
    print("1. Играть с ИИ")
    print("2. Играть с другом")
    print("3. Выход")
    
    choice = input("Выберите режим: ").strip()
    if choice == "1":
        play_with_ai()
    elif choice == "2":
        play_with_friend()
    elif choice == "3":
        print("До свидания!")
        sys.exit()
    else:
        print("Неверный ввод. Попробуйте снова.")
        main()

if name == '__main__':
    main()
