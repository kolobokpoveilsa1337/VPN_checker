import os
import math

def split_file(input_file, output_dir, num_parts=10):
    """
    Разделяет файл на указанное количество частей (по умолчанию 10).
    Сохраняет части в папку output_dir с именами part_01.txt, part_02.txt, ...
    """
    if not os.path.exists(input_file):
        print(f"Ошибка: файл {input_file} не найден.")
        return

    # Создаём папку, если её нет
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    total = len(lines)
    if total == 0:
        print("Файл пуст, разделение не требуется.")
        return

    # Размер каждой части (округляем вверх)
    part_size = math.ceil(total / num_parts)

    for i in range(num_parts):
        start = i * part_size
        end = min(start + part_size, total)
        if start >= total:
            break  # если строк закончились раньше, чем частей
        part_lines = lines[start:end]

        # Имя файла с ведущим нулём: part_01.txt, part_02.txt, ...
        part_filename = f"part_{i+1:02d}.txt"
        part_path = os.path.join(output_dir, part_filename)

        with open(part_path, 'w', encoding='utf-8') as f_out:
            f_out.writelines(part_lines)

        print(f"Создан {part_path} ({len(part_lines)} строк)")

    print(f"Разделение завершено. {min(num_parts, math.ceil(total/part_size))} частей сохранены в папку '{output_dir}'.")

if __name__ == "__main__":
    split_file("all.txt", "split", 10)
