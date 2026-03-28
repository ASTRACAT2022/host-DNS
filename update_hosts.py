def main():
    print("Начало обновления hosts...")
    
    # 1. Считываем данные
    local_rules = read_local_file(BASE_HOSTS_FILE)
    remote_rules = fetch_url(AD_BLOCKLIST_URL)
    
    # 2. Объединяем и убираем дубликаты
    all_rules = set()
    
    for line in local_rules:
        line = line.strip()
        if line and not line.startswith('#'):
            all_rules.add(line)
            
    for line in remote_rules:
        line = line.strip()
        if line.startswith('0.0.0.0') or line.startswith('127.0.0.1'):
            all_rules.add(line)

    # 3. Сортируем для красоты
    sorted_rules = sorted(list(all_rules))

    # 4. Формируем итоговый файл
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        # === ТВОЙ КАСТОМНЫЙ ХЕДЕР ===
        f.write("# Авто-обновленный hosts файл\n")
        f.write(f"# Последнее обновление: {current_date}\n")
        f.write(f"# Источник рекламы: {AD_BLOCKLIST_URL}\n")
        f.write("#ASTRACAT.RU t.me/astracatuo\n")  
        f.write("\n")  
        # =============================
        
        # Записываем все правила
        for rule in sorted_rules:
            f.write(f"{rule}\n")

    print(f"Готово! Записано {len(sorted_rules)} правил в {OUTPUT_FILE}")
