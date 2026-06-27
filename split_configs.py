import os
import math

def split_file(input_file, output1, output2):
    """Разделяет файл на две равные части по количеству строк."""
    if not os.path.exists(input_file):
        print(f"Файл {input_file} не найден.")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    total = len(lines)
    half = math.ceil(total / 2)  # если нечётное, первая часть будет на 1 строку больше

    with open(output1, 'w', encoding='utf-8') as f1:
        f1.writelines(lines[:half])

    with open(output2, 'w', encoding='utf-8') as f2:
        f2.writelines(lines[half:])

    print(f"Файл {input_file} ({total} строк) разделён на {output1} ({half} строк) и {output2} ({total - half} строк)")

if __name__ == "__main__":
    split_file("all.txt", "part1.txt", "part2.txt")
