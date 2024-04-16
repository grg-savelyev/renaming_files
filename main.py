import os
import glob
import re


def rename_files(data, path) -> str:
    for old_name, new_name in data.items():
        # сборка старой и новой ссылок на файл
        old_txt_path = os.path.join(path, f"{old_name}.txt")
        new_txt_path = os.path.join(path, f"{new_name}.txt")
        old_pdf_path = os.path.join(path, f"{old_name}.pdf")
        new_pdf_path = os.path.join(path, f"{new_name}.pdf")

        # переименовывание файлов, если они существуют
        if os.path.exists(old_txt_path):
            os.rename(old_txt_path, new_txt_path)
        if os.path.exists(old_pdf_path):
            os.rename(old_pdf_path, new_pdf_path)
    return 'Обработка завершена'


def creates_filenames(txt_files) -> dict:
    """Создание словаря data, где k - имя txt файла сейчас, v - новое название (арт, характеристика)."""
    data = {}
    for txt_file in txt_files:
        old_name = os.path.basename(txt_file)
        item, characteristic, total_codes = None, None, 0  # новое имя файла — артикул, характеристика, всего qr-кодов

        with open(txt_file, 'r', encoding='utf-8') as file:
            for line in file.readlines():
                line = line.strip()

                # поиск артикула
                pattern = r'Артикул:\s+(\d+)'
                match = re.search(pattern, line)
                if match:
                    if not item in (None, item):
                        raise ValueError(f'Найдены разные артикула в {txt_file}')
                    item = match.group(1).replace(' / ', '_')

                # поиск характеристики
                pattern = r'[а-я]+ / [a-z]+, \d{2}(?=\s)'
                match = re.search(pattern, line)
                if match:
                    if not characteristic in (None, characteristic):
                        raise ValueError(f'Найдены разные характеристики в {txt_file}')
                    characteristic = match.group(0).replace(' / ', '_')

                # подсчет кодов
                pattern = r'0469\d{10}(?!\(21\))'
                match = re.search(pattern, line)
                if match:
                    total_codes += 1

        if not total_codes:
            raise ValueError("ШК не найдены")
        data[old_name.rstrip('.txt')] = f'{item}, {characteristic} - {total_codes}'
    return data


def collect_txt_files(path) -> list:
    """Формирование списка всех файлов с расширением txt внутри указанной папки в виде ссылок."""
    return glob.glob(os.path.join(path, '*.txt'))


def main():
    print('Укажите путь к папке для обработки:')
    folder_path = r'C:\Users\Lenovo\Desktop\КМ артикула 86575, Xiamen Tengfei Imp. and Exp. Co., Ltd'
    print('Запуск обработки.\n')
    txt_files = collect_txt_files(folder_path)
    data = creates_filenames(txt_files)
    print(txt_files)
    print(data)
    print(rename_files(data, folder_path))


if __name__ == "__main__":
    main()
