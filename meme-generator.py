from bs4 import BeautifulSoup
import requests
import os


def create_directory(directory):
    """Создает директорию, если она не существует."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def download_images(url, folder_path):
    """Скачивает изображения с указанного URL и сохраняет их в указанную директорию."""
    response = requests.get(url=url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')

    cards = soup.find_all('div', class_='card')

    for card in cards:
        img_tags = card.find_all('img')
        
        for img in img_tags:
            img_url = img.get('src')
            
            if img_url:
                img_name = os.path.basename(img_url)
                img_data = requests.get(img_url).content
                
                with open(os.path.join(folder_path, img_name), 'wb') as f:
                    f.write(img_data)
                    print(f"Изображение {img_name} сохранено успешно.")


if __name__ == "__main__":
    url = 'https://www.memify.ru/highfive/'
    create_directory("meme_images")
    download_images(url, "meme_images")
