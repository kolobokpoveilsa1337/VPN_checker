import requests
import re
from urllib.parse import urlparse

def fix_ipv6_url(url):
    """
    Проверяет, содержит ли URL IPv6-адрес без квадратных скобок.
    Если да — добавляет их.
    """
    try:
        parsed = urlparse(url)
        host = parsed.hostname
        # Если хост содержит ':' и не заключён в скобки, это IPv6
        if host and ':' in host and not host.startswith('['):
            # Экранируем хост
            netloc = f"[{host}]"
            if parsed.port:
                netloc += f":{parsed.port}"
            # Пересобираем URL
            fixed = parsed._replace(netloc=netloc).geturl()
            return fixed
        return url
    except Exception:
        return url

def extract_key(line):
    """
    Извлекает (scheme, host, port) из строки-конфига.
    Умеет обрабатывать IPv6-адреса как с квадратными скобками, так и без них.
    """
    line = line.strip()
    if re.match(r'^[a-zA-Z0-9+.-]+://', line):
        try:
            parsed = urlparse(line)
            host = parsed.hostname
            port = parsed.port
            if host and port:
                # Если хост содержит ':' и не начинается с '[', то это IPv6 без скобок — экранируем для ключа
                if ':' in host and not host.startswith('['):
                    # Экранируем для хранения ключа
                    host = f"[{host}]"
                return (parsed.scheme, host, port)
        except Exception:
            pass
    # fallback: ищем HOST:PORT (может быть IPv6 без скобок, но редко)
    match = re.search(r'([a-zA-Z0-9.:-]+):(\d+)', line)
    if match:
        host = match.group(1)
        port = int(match.group(2))
        if ':' in host and not host.startswith('['):
            host = f"[{host}]"
        return ('unknown', host, port)
    return None

def main():
    # Читаем ссылки из файла urls.txt
    with open("urls.txt", "r", encoding="utf-8") as f:
        links = [line.strip() for line in f if line.strip()]

    seen = set()
    unique_lines = []

    for url in links:
        # Исправляем URL, если в нём есть IPv6 без скобок
        fixed_url = fix_ipv6_url(url)
        print(f"Загрузка: {fixed_url}")
        try:
            resp = requests.get(fixed_url, timeout=30)
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
