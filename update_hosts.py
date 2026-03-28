import requests
import datetime

# --- НАСТРОЙКИ ---
BASE_HOSTS_FILE = 'base_hosts.txt'
OUTPUT_FILE = 'hosts'
# Вставь сюда прямую ссылку на raw-файл с блокировщиком (например, Steven Black или AdAway)
AD_BLOCKLIST_URL = 'https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts' 

def fetch_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text.splitlines()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при скачивании {url}: {e}")
        return []

def read_local_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read().splitlines()
    except FileNotFoundError:
        print(f"Файл {filename} не найден. Создайте его.")
        return []

def main():
    print("Начало обновления hosts...")
    
    # 1. Считываем данные
    local_rules = read_local_file(BASE_HOSTS_FILE)
    remote_rules = fetch_url(AD_BLOCKLIST_URL)
    
    # 2. Объединяем и убираем дубликаты (используем set для уникальности)
    # Оставляем только непустые строки
    all_rules = set()
    
    for line in local_rules:
        line = line.strip()
        if line and not line.startswith('#'): # Игнорируем комментарии в базовом файле, если нужно
            all_rules.add(line)
            
    for line in remote_rules:
        line = line.strip()
        # Фильтруем: берем только строки, которые выглядят как правила блокировки (начинаются с 0.0.0.0 или 127.0.0.1)
        # И пропускаем заголовки самого скачанного файла
        if line.startswith('0.0.0.0') or line.startswith('127.0.0.1'):
            all_rules.add(line)

    # 3. Сортируем для красоты
    sorted_rules = sorted(list(all_rules))

    # 4. Формируем итоговый файл
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(f"# Авто-обновленный hosts файл\n")
        f.write(f"# Последнее обновление: {current_date}\n")
        f.write(f"# Источник рекламы: {AD_BLOCKLIST_URL}\n\n")
        
        # Снова добавляем базовые правила в начало (если они были в set, порядок мог сбиться, но мы их уже добавили)
        # Для простоты просто пишем всё отсортированное множество
        for rule in sorted_rules:
            f.write(f"{rule}\n")

    print(f"Готово! Записано {len(sorted_rules)} правил в {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
