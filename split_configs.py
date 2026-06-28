import os
import math

def split_into_parts(input_file, num_parts=6):
    """Разделяет файл на num_parts частей (почти равных по количеству строк)."""
    if not os.path.exists(input_file):
        print(f"Файл {input_file} не найден.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    total = len(lines)
    if total == 0:
        print("Файл пуст, создаём пустые части.")
        for i in range(1, num_parts + 1):
            with open(f"part{i}.txt", 'w', encoding='utf-8') as f:
                f.write("")
        return

    # Размер каждой части (округляем вверх)
    part_size = math.ceil(total / num_parts)

    for i in range(num_parts):
        start = i * part_size
        end = min((i + 1) * part_size, total)
        part_lines = lines[start:end]
        out_filename = f"part{i+1}.txt"
        with open(out_filename, 'w', encoding='utf-8') as f:
            f.writelines(part_lines)
        print(f"Записано {len(part_lines)} строк в {out_filename}")

    print(f"Файл {input_file} ({total} строк) разделён на {num_parts} частей.")

if __name__ == "__main__":
    # Можно поменять число здесь, если нужно другое количество
    split_into_parts("all.txt", num_parts=6)
