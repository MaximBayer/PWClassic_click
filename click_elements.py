import cv2
import numpy as np
import pyautogui
import time
import pytesseract
import os

# Вкажіть шлях до Tesseract OCR, якщо потрібно
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Отримуємо поточну директорію скрипта
script_dir = os.path.dirname(os.path.abspath(__file__))

# Завантаження шаблонів зображень без підпапки
templates = []
for i, filename in enumerate(['image1.png', 'image2.png', 'image3.png']):
    path = os.path.join(script_dir, filename)
    
    # Додаємо перевірку існування файлу
    if not os.path.exists(path):
        print(f"[ERROR] Файл не знайдено за шляхом: {path}")
        continue  # пропустити файл, якщо його не існує
    
    print(f"[INFO] Завантаження зображення: {path}")
    image = cv2.imread(path, cv2.IMREAD_COLOR)
    
    if image is not None:
        templates.append({'image': image, 'name': f"зображення {i + 1}"})
    else:
        print(f"[ERROR] Cannot load image: {path}")

# Перевірка, чи завантажилися всі зображення
if not templates:
    print("[ERROR] No images were loaded. Please check the paths.")
    exit()

# Список текстів, які потрібно шукати на екрані
text_templates = ["Готов!", "Готов!", "Выбрать!"]

# Функція для попередньої обробки зображення
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray

# Функція для пошуку шаблону зображення на екрані
def find_and_click_image(screenshot, template, threshold=0.98):
    template_processed = preprocess_image(template)
    result = cv2.matchTemplate(screenshot, template_processed, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        x, y = max_loc
        w, h = template.shape[1], template.shape[0]
        pyautogui.click(x + w // 2, y + h // 2)
        return True
    return False

# Функція для пошуку тексту на екрані
def find_and_click_text(screenshot_rgb, text_templates):
    detected_text = pytesseract.image_to_string(screenshot_rgb)
    
    for text in text_templates:
        if text in detected_text:
            print(f"Знайдено та натиснуто на текст: {text}")
            return True
    return False

# Основний цикл
while True:
    screenshot = pyautogui.screenshot()
    screenshot_np = np.array(screenshot)
    screenshot_gray = preprocess_image(screenshot_np)
    screenshot_rgb = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

    for template in templates:
        if find_and_click_image(screenshot_gray, template['image']):
            print(f"Знайдено та натиснуто на {template['name']} image!")

    if find_and_click_text(screenshot_rgb, text_templates):
        print("Знайдено та натиснуто на текстовий елемент!")
    
    time.sleep(0.1)
