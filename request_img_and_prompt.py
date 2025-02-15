# pip install requests

# source NEUROCHAGEIMAGES/bin/activate

import requests
import os
import base64

# Определяем адрес сервера
server = 'http://192.168.100.149:5005'  # Измените на IP-адрес вашего сервера

# Указываем имя файла изображения и полный путь
old_name = 'dog.jpg'  # Полный путь к файлу изображения

# Проверяем, существует ли указанный файл изображения
if os.path.isfile(old_name):
    print(f"Файл {old_name} найден.")
else:
    print(f"Файл {old_name} не найден.")
    exit(1)  # Выход, если файл не найден

# Читаем файл изображения и кодируем его в base64
with open(old_name, 'rb') as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

# Отправляем данные изображения на сервер
response = requests.post(f"{server}/upload_image", json={"image_data": encoded_string, "image_name": os.path.basename(old_name)})

# Проверяем код состояния ответа
if response.status_code == 200:
    print("Изображение успешно загружено:", response.json())
    generated_image_path = response.json().get('image_path')
    
    # Скачиваем сгенерированное изображение
    filename = os.path.basename(generated_image_path)  # Получаем имя файла
    download_response = requests.get(f"{server}/download_image/{filename}")

    if download_response.status_code == 200:
        with open(f"downloaded_{filename}", 'wb') as f:
            f.write(download_response.content)
        print(f"Сгенерированное изображение успешно скачано как downloaded_{filename}")
    else:
        print(f"Ошибка при скачивании изображения: {download_response.status_code}, Ответ: {download_response.text}")
else:
    print(f"Ошибка: {response.status_code}, Ответ: {response.text}")
