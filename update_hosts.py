import requests
import datetime

# --- НАСТРОЙКИ ---
BASE_HOSTS_FILE = 'base_hosts.txt'
OUTPUT_FILE = 'bypass'  # Имя итогового файла
# Ссылка на список блокировки рекламы (можно заменить на любой другой)
AD_BLOCKLIST_URL = 'https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts' 

def fetch_url(url):
    """Скачивает файл по ссылке и возвращает список строк"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text.splitlines()
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Ошибка при скачивании {url}: {e}")
        return []

def read_local_file(filename):
    """Читает локальный файл и возвращает список строк"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read().splitlines()
    except FileNotFoundError:
        print(f"⚠️ Файл {filename} не найден. Создайте его с вашими правилами.")
        return []

def main():
    print("🔄 Начало обновления bypasss...")
    
    # 1. Считываем данные
    local_rules = read_local_file(BASE_HOSTS_FILE)
    remote_rules = fetch_url(AD_BLOCKLIST_URL)
    
    # 2. Объединяем и убираем дубликаты
    all_rules = set()
    
    # Добавляем правила из локального файла (пропускаем пустые строки и комментарии)
    for line in local_rules:
        line = line.strip()
        if line and not line.startswith('#'):
            all_rules.add(line)
            
    # Добавляем правила из удалённого списка (только валидные правила блокировки)
    for line in remote_rules:
        line = line.strip()
        if line.startswith('0.0.0.0') or line.startswith('127.0.0.1'):
            all_rules.add(line)

    # 3. Сортируем правила для читаемости
    sorted_rules = sorted(list(all_rules))

    # 4. Формируем итоговый файл с кастомным хедером
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        # === КАСТОМНЫЙ ХЕДЕР ===
        f.write("# Авто-обновленный hosts файл\n")
        f.write(f"# Последнее обновление: {current_date}\n")
        f.write(f"# Источник рекламы: {AD_BLOCKLIST_URL}\n")
        f.write("# ASTRACAT.RU t.me/astracatuo\n")
        f.write("\n")
        # =======================
        
        # Записываем все правила
        for rule in sorted_rules:
            f.write(f"{rule}\n")

    print(f"✅ Готово! Записано {len(sorted_rules)} правил в файл '{OUTPUT_FILE}'")

if __name__ == "__main__":
    main()
