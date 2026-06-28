import requests
import re
from urllib.parse import urlparse

def extract_key(line):
    line = line.strip()
    if re.match(r'^[a-zA-Z0-9+.-]+://', line):
        parsed = urlparse(line)
        scheme = parsed.scheme
        host = parsed.hostname
        port = parsed.port
        if host and port:
            return (scheme, host, port)
    # fallback: ищем HOST:PORT
    match = re.search(r'([a-zA-Z0-9.-]+):(\d+)', line)
    if match:
        return ('unknown', match.group(1), int(match.group(2)))
    return None
def main():
    # Читаем ссылки из файла urls.txt
    with open("urls.txt", "r", encoding="utf-8") as f:
        links = [line.strip() for line in f if line.strip()]

    seen = set()
    unique_lines = []

    for url in links:
        print(f"Загрузка: {url}")
        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            for line in resp.text.splitlines():
                line = line.strip()
                if not line:
                    continue

                key = extract_key(line)
                if key is None:
                    key = line  # точное совпадение

                if key not in seen:
                    seen.add(key)
                    unique_lines.append(line)
        except Exception as e:
            print(f"Ошибка при загрузке {url}: {e}")

    # Сохраняем результат в all.txt
    with open("all.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(unique_lines))

    print(f"Готово! Уникальных конфигов: {len(unique_lines)}")

if __name__ == "__main__":
    main()
