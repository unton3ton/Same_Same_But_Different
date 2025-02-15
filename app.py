# https://huggingface.co/stabilityai/stable-diffusion-2-depth

# https://github.com/huggingface/diffusers/blob/main/docs/source/en/api/pipelines/stable_diffusion/stable_diffusion_2.md?ysclid=m709apofgc89030639
# https://github.com/Dmukherjeetextiles/background-remover/blob/main/app.py


# https://dev.to/jeremycmorgan/how-to-generate-ai-images-with-stable-diffusion-xl-in-5-minutes-4ael?ysclid=m705xex0wu329090478
# https://requests.readthedocs.io/en/latest/user/quickstart/
# https://timeweb.cloud/tutorials/python/vvedenie-v-rabotu-s-bibliotekoj-requests-v-python?ysclid=m70gsl6zpl441410737
# https://stackoverflow.com/questions/17733133/loading-image-from-flasks-request-files-attribute-into-pil-image
# https://python-scripts.com/requests?ysclid=m70b2l58ex730107366



# pip install --upgrade pip
# pip install --upgrade diffusers[torch]
# pip install transformers Flask requests


from flask import Flask, request, jsonify, send_file
import os
import base64
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler, FluxPipeline
import torch
from PIL import Image
from io import BytesIO
import ollama

app = Flask(__name__)

# Директория для сохранения загруженных изображений
UPLOAD_FOLDER = 'uploaded_images'  # Измените на желаемую директорию
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Создаем директорию, если она не существует

# Загружаем модель диффузии
pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-schnell", torch_dtype=torch.bfloat16)
# repo_id = "stabilityai/stable-diffusion-2-base"
# pipe = DiffusionPipeline.from_pretrained(repo_id, torch_dtype=torch.float16, variant="fp16")
# pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
# pipe = pipe.to("cuda")

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if request.method == 'POST':
        data = request.get_json()
        if 'image_data' not in data or 'image_name' not in data:
            return jsonify({'error': 'Отсутствуют данные изображения или имя изображения'}), 400
        
        image_data = data['image_data']
        image_name = data['image_name']

        # Декодируем данные изображения в base64
        try:
            image_bytes = base64.b64decode(image_data)
            image_path = os.path.join(UPLOAD_FOLDER, image_name)
            with open(image_path, 'wb') as img_file:
                img_file.write(image_bytes)

            print(f"Изображение сохранено по пути: {image_path}")

            # Создаем описание для выходного изображения
            response = ollama.chat(
                model='llama3.2-vision',
                messages=[{
                    'role': 'user',
                    'content': 'What is in this image?',
                    'images': [image_path]  # Убедитесь, что путь правильный
                }]
            )

            # Проверяем, есть ли ответ от модели
            if 'message' not in response or 'content' not in response['message']:
                return jsonify({'error': 'Не удалось получить ответ от модели'}), 400
            
            # Генерируем изображение с помощью модели диффузии
            prompt = response['message']['content']
            print(f"Полученный запрос: {prompt}")
            generated_image = pipe(prompt, num_inference_steps=42).images[0]

            # Сохраняем сгенерированное изображение
            output_path = os.path.join(UPLOAD_FOLDER, f"generated_{image_name}")
            generated_image.save(output_path)

            # Подтверждаем, что изображение было сохранено
            if os.path.isfile(output_path):
                print(f"Изображение успешно сохранено: {output_path}")
            else:
                print(f"Не удалось сохранить изображение: {output_path}")

            return jsonify({'status': 'success', 'image_path': output_path}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500  # Возвращаем сообщение об ошибке

@app.route('/download_image/<filename>', methods=['GET'])
def download_image(filename):
    # Путь к сгенерированному изображению
    image_path = os.path.join(UPLOAD_FOLDER, filename)
    
    if not os.path.isfile(image_path):
        return jsonify({'error': 'Файл не найден'}), 404
    
    return send_file(image_path, mimetype='image/jpeg')  # Убедитесь, что тип MIME соответствует вашему изображению


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
  # Запускаем сервер на всех интерфейсах

