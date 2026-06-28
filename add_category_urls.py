import requests
import re
import os

def get_raw_links_from_category():
    """
    Парсит страницу https://github.com/mohamadfg-dev/telegram-v2ray-configs-collector/tree/main/category
    и возвращает список сырых ссылок на все .txt файлы.
    """
    url = "https://github.com/mohamadfg-dev/telegram-v2ray-configs-collector/tree/main/category"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        html = response.text

        # Ищем все ссылки вида /mohamadfg-dev/telegram-v2ray-configs-collector/blob/main/category/имя_файла.txt
        # Паттерн ищет href, где в конце .txt и содержится /blob/main/category/
        pattern = r'href="(/mohamadfg-dev/telegram-v2ray-configs-collector/blob/main/category/[^"]+\.txt)"'
        matches = re.findall(pattern, html)

        raw_links = []
        for blob_url in matches:
            # Преобразуем blob в raw: заменяем /blob/ на /raw/
            raw_url = blob_url.replace("/blob/", "/raw/")
            full_raw_url = "https://raw.githubusercontent.com" + raw_url
            raw_links.append(full_raw_url)

        # Удаляем дубликаты (на всякий случай)
        raw_links = list(dict.fromkeys(raw_links))
        return raw_links

    except Exception as e:
        print(f"[Ошибка] Не удалось получить список файлов: {e}")
        return []

def update_urls_file(new_links, urls_file="urls.txt"):
    """
    Добавляет новые ссылки в urls.txt, избегая дубликатов.
    """
    # Читаем существующие ссылки
    existing = set()
    if os.path.exists(urls_file):
        with open(urls_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    existing.add(line)

    # Добавляем новые
    added = 0
    for link in new_links:
        if link not in existing:
            existing.add(link)
            added += 1

    # Записываем обратно (сортируем для удобства)
    with open(urls_file, 'w', encoding='utf-8') as f:
        for link in sorted(existing):
            f.write(link + '\n')

    print(f"[Готово] Добавлено {added} новых ссылок. Всего ссылок: {len(existing)}")

if __name__ == "__main__":
    print("[INFO] Загружаем список .txt файлов из category...")
    links = get_raw_links_from_category()
    print(f"[INFO] Найдено {len(links)} файлов.")

    if links:
        update_urls_file(links)
    else:
        print("[WARN] Не найдено ни одного файла. Проверьте доступность страницы.")
