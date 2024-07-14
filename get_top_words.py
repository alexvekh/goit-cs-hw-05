# Напишіть Python-скрипт, який завантажує текст із заданої URL-адреси, 
# аналізує частоту використання слів у тексті за допомогою парадигми MapReduce 
# і візуалізує топ-слова з найвищою частотою використання у тексті.

# Покрокова інструкція

# Імпортуйте необхідні модулі (matplotlib та інші).
# Візьміть код реалізації MapReduce з конспекту.
# Створіть функцію visualize_top_words для візуалізації результатів.
# У головному блоці коду отримайте текст за URL, застосуйте MapReduce та візуалізуйте результати.

# Критерії прийняття
# - Код успішно завантажує текст із заданої URL-адреси.
# - Код коректно виконує аналіз частоти слів із використанням MapReduce.
# - Візуалізація відображає топ-слова за частотою використання.
# - Код ефективно використовує багатопотоковість.
# - Код читабельний та відповідає стандартам PEP 8.

# Вдосконалимо наш MapReduce та виконаємо наступні кроки. 
# По-перше, додамо функцію для видалення знаків пунктуації. Це необхідно, щоб правильно розділити текст на слова, ігноруючи знаки пунктуації. 
# Другим кроком виконаємо модифікацію функції map_reduce. 
# Тепер вона буде приймати необов'язковий аргумент — список слів, для яких потрібно підрахувати кількість входження. 
# Якщо список не задано, функція буде підраховувати входження всіх слів у тексті.

import string

from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

import requests

import matplotlib.pyplot as plt

def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Перевірка на помилки HTTP
        return response.text
    except requests.RequestException as e:
        return None


# Функція для видалення знаків пунктуації з тексту перед тим, як він буде оброблений функцією MapReduce. 
# Це забезпечує точніший підрахунок слів.
def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))


def map_function(word):
    return word, 1


def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()


def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)


# Виконання MapReduce
# Також змінилися логіка виконання функції map_reduce. Тепер вона перевіряє, чи задано список слів для пошуку. 
# Якщо так, то функція враховує тільки ці слова, ігноруючи інші. 
# Це дозволяє використовувати MapReduce для пошуку конкретних слів, а не для підрахунку всіх слів у тексті.
def map_reduce(text, search_words=None):
    # Видалення знаків пунктуації
    text = remove_punctuation(text)
    words = text.split()

    # Виключення артиклів
    articles = {'the', 'a', 'an', 'of', 'to', 'and', 'in', 'it', 'that', 'not', 'as', 'is', 'at', 'for', 'but', 'on', 'or', 'by', 'from'}
    words = [word for word in words if word.lower() not in articles]

    # Приведення всіх слів до нижнього регістру
    words = [word.lower() for word in words]

    # Якщо задано список слів для пошуку, враховувати тільки ці слова
    if search_words:
        words = [word for word in words if word in search_words]

    # Паралельний Маппінг
    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    # Крок 2: Shuffle
    shuffled_values = shuffle_function(mapped_values)

    # Паралельна Редукція
    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)

# Функція побудови графіка
def visualize_top_words(result, top_n=20):
    # Visualize the top 10 words and their frequencies using a horizontal bar chart ((dict), top_n=10 ) 

    # Sort the word frequencies dictionary by frequency in descending order and select the top N words
    sorted_words = sorted(result.items(), key=lambda item: item[1], reverse=True)[:top_n]

    # Separate the words and their frequencies for plotting
    words, frequencies = zip(*sorted_words)

    # Create a horizontal bar chart
    plt.figure(figsize=(10, 8))
    plt.barh(words, frequencies, color='skyblue')
    plt.xlabel('Frequency')
    plt.ylabel('Words')
    plt.title(f'Top {top_n} Most Frequent Words')
    plt.gca().invert_yaxis()  # Invert y-axis to have the highest frequency word at the top
    plt.show()



if __name__ == "__main__":
    # Вхідний текст для обробки
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    text = get_text(url)
    if text:
        # Виконання MapReduce на вхідному тексті
        
        search_words = ["war", "peace", "love"]
        search_words2 = ["war", "peace", "love", "people", "must", "hands"]
        result = map_reduce(text)

        print('слів:', result.__len__())

        print("Результат підрахунку слів:", result)
        print('Слів в тексті:', text.__len__())
        print('Слів в різних:', result.__len__())
        visualize_top_words(result)
    else:
        print("Помилка: Не вдалося отримати вхідний текст.")
    