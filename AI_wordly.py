import random
from transformers import pipeline
import pymorphy2
from termcolor import colored

# Дополнительная автономная поддержка викисловаря
try:
    from pyzim.reader import Archive
    import mwparserfromhell
    wiktionary = Archive('ruwiktionary.zim')
    OFFLINE_DICT_ENABLED = True
except Exception as e:
    print("Offline Wiktionary not loaded:", e)
    wiktionary = None
    OFFLINE_DICT_ENABLED = False

# Настройка морфологического анализатора русского языка
morph = pymorphy2.MorphAnalyzer()

# Инициализировать GPT-конвейер (должен быть установлен PyTorch или TensorFlow)
def init_gpt_pipeline():
    try:
        return pipeline("text-generation", model="sberbank-ai/rugpt3small_based_on_gpt2")
    except Exception as e:
        print("Ошибка загрузки модели GPT:", e)
        return None

text_gen = init_gpt_pipeline()

# Сгенерируйте русское существительное с помощью GPT
def generate_russian_word_gpt():
    if not text_gen:
        raise RuntimeError("GPT pipeline is not initialized")

    prompt = "Придумай одно существительное из 5 букв на русском языке. Только слово."
    result = text_gen(prompt, max_length=10, do_sample=True, top_k=50)[0]['generated_text']
    word = result.strip().split()[0].lower()
    return word

# Подтверждение значения существительного с помощью pymorphy2 и, при необходимости, Викисловаря
def is_noun(word):
    parsed = morph.parse(word)[0]
    is_valid_noun = 'NOUN' in parsed.tag and len(word) == 5

    if OFFLINE_DICT_ENABLED:
        try:
            entry = wiktionary.get_entry_by_title(word)
            if entry:
                content = entry.read()
                if "существительное" in content:
                    return is_valid_noun
        except:
            pass

    return is_valid_noun

# Обратная связь пользовательского интерфейса для словоподобного ответа
def display_guess(guess, target):
    feedback = ""
    for i, letter in enumerate(guess):
        if letter == target[i]:
            feedback += colored(letter, 'green')
        elif letter in target:
            feedback += colored(letter, 'yellow')
        else:
            feedback += colored(letter, 'white')
    print(feedback)

def play_game(target_word, max_tries=6, hints=0):
    print("Угадайте слово из 5 букв (на русском):")
    attempts = 0
    while attempts < max_tries or max_tries == -1:
        guess = input(f"Попытка {attempts + 1}: ").strip().lower()
        if len(guess) != 5:
            print("Введите слово из 5 букв.")
            continue
        display_guess(guess, target_word)
        if guess == target_word:
            print("Поздравляем! Вы угадали слово!")
            return
        attempts += 1
    print(f"Вы проиграли. Загаданное слово было: {target_word}")

# Основное выполнение
if name == "__main__":
    try:
        word = generate_russian_word_gpt()
        while not is_noun(word):
            word = generate_russian_word_gpt()
    except Exception as e:
        print("Не удалось получить слово от GPT. Ошибка:", e)
        word = random.choice(["город", "школа", "мосты", "лампа", "песня"])

    play_game(target_word=word, max_tries=10, hints=1)
