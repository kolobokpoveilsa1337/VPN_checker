import os
import math

def split_file(input_file, output_dir, num_parts=5):   # теперь по умолчанию 5
    if not os.path.exists(input_file):
        print(f"Ошибка: файл {input_file} не найден.")
        return

    # Если существует файл с именем output_dir – удаляем его, чтобы создать папку
    if os.path.exists(output_dir) and not os.path.isdir(output_dir):
        os.remove(output_dir)
        print(f"Удалён файл-помеха: {output_dir}")

    os.makedirs(output_dir, exist_ok=True)   # теперь папка создаётся без ошибок

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    total = len(lines)
    if total == 0:
        print("Файл пуст, разделение не требуется.")
        return

    part_size = math.ceil(total / num_parts)

    for i in range(num_parts):
        start = i * part_size
        end = min(start + part_size, total)
        if start >= total:
            break
        part_lines = lines[start:end]
        part_filename = f"part_{i+1:02d}.txt"
        part_path = os.path.join(output_dir, part_filename)

        with open(part_path, 'w', encoding='utf-8') as f_out:
            f_out.writelines(part_lines)

        print(f"Создан {part_path} ({len(part_lines)} строк)")

    print(f"Разделение завершено. {min(num_parts, math.ceil(total/part_size))} частей сохранены в папку '{output_dir}'.")

if __name__ == "__main__":
    split_file("all.txt", "split", 5)   # теперь 5 частей
