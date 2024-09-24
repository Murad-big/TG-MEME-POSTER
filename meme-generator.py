from bs4 import BeautifulSoup
import requests
import os

def create_directory(directory):
    """Создает директорию, если она не существует."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def download_images(url, folder_path):
    """Скачивает изображения с указанного URL и сохраняет их в указанную директорию."""
    # Отправляем GET-запрос к указанной странице
    response = requests.get(url=url)
    # Устанавливаем кодировку ответа сервера в UTF-8 для корректного отображения текста на кириллице
    response.encoding = 'utf-8'
    # Преобразуем текст ответа сервера в объект BeautifulSoup с использованием парсера 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')

    # Ищем все элементы <div> с классом 'card' на странице
    cards = soup.find_all('div', class_='card')

    # Проходимся по найденным элементам <div> с классом 'card' и ищем в них все теги <img>
    for card in cards:
        img_tags = card.find_all('img')
        for img in img_tags:
            img_url = img.get('src')
            # Проверяем, что у изображения есть URL
            if img_url:
                # Получаем имя файла из URL
                img_name = os.path.basename(img_url)
                # Скачиваем изображение
                img_data = requests.get(img_url).content
                # Сохраняем изображение в папку
                with open(os.path.join(folder_path, img_name), 'wb') as f:
                    f.write(img_data)
                    print(f"Изображение {img_name} сохранено успешно.")

# Основная логика программы
if __name__ == "__main__":
    # Задаем URL-адрес веб-страницы для парсинга
    url = 'https://www.memify.ru/highfive/'
    # Создаем директорию для сохранения изображений, если её еще нет
    create_directory("meme_images")
    # Вызываем функцию для скачивания изображений
    download_images(url, "meme_images")