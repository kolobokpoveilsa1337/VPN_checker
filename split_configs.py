import os
import math

def split_file(input_file, num_parts=6):
    """
    Разделяет файл на указанное количество частей (по числу строк).
    Части сохраняются как part1.txt, part2.txt, ..., partN.txt.
    Если строк меньше, чем частей, создаются только нужные файлы.
    """
    if not os.path.exists(input_file):
        print(f"Файл {input_file} не найден.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    total = len(lines)
    if total == 0:
        print("Файл пуст, ничего не делаем.")
        return

    # Размер каждой части (округляем вверх, чтобы последняя часть могла быть меньше)
    part_size = math.ceil(total / num_parts)

    for i in range(num_parts):
        start = i * part_size
        end = min(start + part_size, total)
        if start >= total:
            break  # если строк меньше, чем частей, дальше не создаём
        part_filename = f"part{i+1}.txt"
        with open(part_filename, 'w', encoding='utf-8') as f_out:
            f_out.writelines(lines[start:end])
        print(f"Создан {part_filename}: строки {start+1}-{end} (всего {end-start})")

    print(f"Файл {input_file} ({total} строк) разделён на {min(num_parts, total)} частей.")

if __name__ == "__main__":
    split_file("all.txt", num_parts=6)
