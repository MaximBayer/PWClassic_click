import ctypes
import os
import requests
import zipfile
import subprocess
import json
import time
from colorama import init, Fore
from tqdm import tqdm

# Ініціалізація colorama для кольорового тексту в консолі
ctypes.windll.kernel32.SetConsoleTitleA(b"PWClassic_click Loader")
init(autoreset=True)

# Логотип
logo = [
    "PWClassic Clicker Loader",
    "Завантажує та запускає автоматизацію кнопок для гри",
]
for line in logo:
    print(Fore.CYAN + line)

# Функція завантаження та розархівації
def download_and_extract(url, extract_dir):
    response = requests.get(url, stream=True)
    filename = os.path.join(extract_dir, "PWClassic_click.zip")
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    t = tqdm(total=total_size, unit='B', unit_scale=True, desc=filename, leave=True)
    with open(filename, 'wb') as file:
        for data in response.iter_content(block_size):
            t.update(len(data))
            file.write(data)
    t.close()
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    os.remove(filename)
    
    # Повертає шлях до розпакованої папки
    return os.path.join(extract_dir, "PWClassic_click-file")

# Функція запуску команд
def execute_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Помилка виконання команди: {e}")

# Основна функція установки та запуску
def setup_and_run():
    # Отримуємо поточну директорію, де запущено Loader
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Завантаження репозиторію
    target_dir = download_and_extract("https://github.com/MaximBayer/PWClassic_click/archive/refs/heads/file.zip", base_dir)

    # Встановлення залежностей
    print(Fore.YELLOW + "[!] Встановлення залежностей...")
    requirements_path = os.path.join(target_dir, "requirements.txt")
    if os.path.exists(requirements_path):
        execute_command(["pip", "install", "-r", requirements_path])
    else:
        print(Fore.RED + "Файл requirements.txt не знайдено.")

    # Запуск основного скрипта
    click_elements_path = os.path.join(target_dir, "click_elements.py")
    if os.path.exists(click_elements_path):
        print(Fore.GREEN + "[!] Запуск скрипта...")
        execute_command(["python", click_elements_path])
    else:
        print(Fore.RED + "Файл click_elements.py не знайдено.")

if __name__ == "__main__":
    setup_and_run()
