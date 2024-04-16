import os
import glob


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
        item, characteristic, total_codes = 0, '', 0  # новое имя файла — артикул, характеристика, всего qr-кодов
        char_flag = True  # характеристика, флаг перебора
        line_counter = float('inf')  # счет строк — пока не найден артикул, счетчик = бесконечность

        with open(txt_file, 'r', encoding='utf-8') as file:
            for line in file.readlines():
                line = line.strip()
                if line.isdigit() and len(line) == 5 and char_flag:  # первое условие — артикул
                    item = line
                    line_counter = 10
                elif line_counter > 0:
                    line_counter -= 1
                elif line_counter == 0 and char_flag:  # хар-ка на n строке после артикула
                    characteristic = line
                    char_flag = False  # отключение поиска хар-ки

                if '(01)04' in line and '(21)' in line and len(line) == 35:  # подсчет кодов
                    total_codes += 1
        if total_codes > 0:  # если встречается txt без qr-кода, то имя файла не меняется
            data[old_name.rstrip('.txt')] = f'{item}, {characteristic} - {total_codes}'
    return data


def collect_txt_files(path) -> list:
    """Формирование списка всех файлов с расширением txt внутри указанной папки в виде ссылок."""
    return glob.glob(os.path.join(path, '*.txt'))


def input_path() -> str:
    print('Укажите путь к папке для обработки:')
    folder_path = input()
    print('Запуск обработки.\n')
    return folder_path


def main():
    folder_path = input_path()
    txt_files = collect_txt_files(folder_path)
    data = creates_filenames(txt_files)
    print(rename_files(data, folder_path))


if __name__ == "__main__":
    main()
