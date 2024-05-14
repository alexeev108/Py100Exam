# TODO опишите здесь функции для решения задачи
"""Прототип приложения для конвертации валют"""

import json
import os
import requests
import string
import psutil
import typing

SITE = 'https://app.exchangerate-api.com/sign-up'

def disk_finder() -> list[str]:
    """
    Функция выводит список всех доступных локальных дисков на компьютере пользователя при вводе ALL,
    либо список тех дисков, которые пользователь ввел сам.
    :return: список дисков
    """
    while True:
        available_disk = psutil.disk_partitions()
        list_disk = [dp.device for dp in available_disk if dp.fstype == 'NTFS']

        print(f'\nЛокальные диски, доступные для поиска файла с ключом доступа:\n'
              f'{list_disk}')
        drives = input('\nВведите буквы наименований дисков через пробел, для которых хотите проверить \n'
                       'наличие файла key_access.txt, или введите ALL для поиска по всем дискам: ').upper().strip()
        drives_empty_list = []
        if drives == 'ALL':
            drives_empty_list = list_disk
            break
        else:
            split_drives = drives.split()
            set_split_drives = list(set(split_drives))
            split_drives_one = ','.join(set_split_drives)
            empty = []
            for items in split_drives_one:
                if items.isalpha():
                    empty.append(items)
            intersection = list(set(set_split_drives) & set(empty))
            if len(intersection) != 0:
                for x in intersection:
                    if x:
                        drives_empty_list.append(f'{x}:\\')
                break
            else:
                print('\nВы ввели диски, которых нет на вашем компьютере! Повторите, пожалуйста, ввод.\n')
                continue
    return drives_empty_list

def file_finder() -> list[str]:
    """
    Функция ищет файл key_access.txt во всех папках, на тех дисках компьютера пользователя,
    которые он указал в функции disk_finder.
    :return: список, в котором указан полный путь к файлу key_access.txt
    """
    full_path = disk_finder()
    name = 'key_access.txt'
    result = []
    print('\nВыполняется поиск файла...')
    for disk in full_path:
        for root, dirs, files in os.walk(disk):
            if name in files:
                result.append(os.path.join(root, name))
                continue
            else:
                result = result
    return result

def actual_file() -> list[str]:
    """
    Если на компьютере пользователя найдено несколько файлов key_access.txt, в результате
    работы функции file_finder, то функция предлагает пользователю выбрать актуальный файл.
    Получая список из директорий, удаляет все элементы списка, кроме того, который выбрал пользователь
    :return: список, в котором оставлен удинственный актуальный путь к файлу key_access.txt
    """
    actual = file_finder()
    empty = []
    if len(actual) > 1:
        print('\nНайдено несколько файлов:')
        for index, item in enumerate(actual, 1):
            print(f'{index} - {item}')
        actual_number = int(input('\nВыберите актуальный и введите соответствующее число: ').lower().strip())
        for index_actual, item_actual in enumerate(actual, 1):
            if actual_number == index_actual:
                empty.append(item_actual)
                actual_to_return = empty
    elif len(actual) == 1:
        actual_to_return = actual
    else:
        actual_to_return = actual
    return actual_to_return

def key_writer(pretty_path) -> str:
    """
    Получая путь с расположением файла key_access.txt, функция записывает
    в файл введеный пользователем ключ доступа
    :param pretty_path: путь, записанный ввиде строки
    :return: считывает ключ из файла и возвращает ключ ввиде строки
    """
    keys = []
    list_ = pretty_path
    path = list_[0]
    if os.stat(path).st_size > 0:
        with open(path, 'r') as key_file:
            for strings in key_file:
                if strings:
                    while True:
                        print(f'Считываю код доступа {strings}')

                        # Проверка ключа доступа:
                        ver = verify_key(strings)
                        if ver == 'False':
                            while True:
                                rewrite = input('Перезапишите сами ключ доступа в файле!''Перезаписали? Y/N: ').upper().strip()
                                if rewrite == 'Y':
                                    break
                                else:
                                    continue
                            break
                        else:
                            # Если ключ прошел проверку, записываем его в keys:
                            keys.append(strings)
                            break
                    break
    else:
        print(f'Файл пустой!\n'
                f'Вам надо пройти регистрацию по ссылке: {SITE} и получить ключ доступа')

        # Проверка ключа доступа:
        while True:
            key_enter = input("Введите ключ доступа (Your API Key): ").lower().strip()
            if verify_key(key_enter) == False:
                continue
            else:
                break

        # Если ключ прошел проверку, записываем его в файл и keys:
        with open(path, 'w') as empty_file:
            print(f'Записываю код доступа {key_enter} в файл {empty_file}')
            empty_file.write(key_enter)
        with open(path, 'r') as key_file:
            for strings in key_file:
                if strings:
                    keys.append(strings)
    for key_item in keys:
        str(key_item)
    return key_item

def new_file_creator(choose_key_second) -> str:
    """
    Функция считывает путь, по которому лежит файл программы app.py и создает папку с файлом key_access.txt
    :return: путь, по которому лежит созданный файл с ключом доступа
    """
    filepath = os.getcwd()
    new_filepath = f'{filepath}'+'\\key_access\\key_access.txt'
    if not os.path.exists(f'{filepath}'+'\\key_access'):
        os.makedirs(f'{filepath}'+'\\key_access')
    with open(new_filepath, "w") as new_file:
        new_file.write(choose_key_second)
    return new_filepath

# Далее написана очень важная функция Меню, через которое происходит общение с пользователем

def menu(empty_key) -> list[str]:
    """
    В данной функции реализовано меню выбора для общения с пользователем
    для основной функции converter()

    Пользователь вводит число и функция:
    1:
    - Выполняет поиск файла key_access.txt с ключом доступа или без ключа доступа на компьютере пользователя.
    - Считывает ключ доступа из файла key_access.txt, либо если файл пуст, предлагает выбрать другой пункт меню.
    - Если на компьютере пользователя несколько файлов key_access.txt с ключом доступа, то предлагает
      выбрать актуальный с помощью функции actual_file и считывает ключ доступа из актуального файла key_access.txt.
    - Либо, если пользователя ничего не устраивает из предложенного, предлагает выбрать другой пункт меню.

    2:
    - Пользователь вводит ключ доступа и функция записывает его в файл key_access.txt, или создает
    новый файл key_access.txt с ключом на компьютере пользователя, с помощью функции new_file_creator.
    - Функция считывает ключ доступа из файла key_access.txt.

    3:
    - У пользователя уже есть ключ доступа, файлов key_access.txt у него нет на компьютере и он хочет сразу
      перейти к конвертации.
    - Функция считывает введенный пользователем ключ доступа и перебрасывает программу к конвертации

    4:
    - У пользователя нет ключа доступа. Предлагается получить ключ доступа, зарегистрировавшись на сайте,
      Далее можно создать файл key_access.txt, записать в него ключ доступа, либо, если пользователь сам записал
      ключ в файл, найти этот файл на компьютере пользователя

    :param empty_key: в начале получаем пустой список []
    :return: список с ключом
    """
    while True:
        first_unswer = ['У меня уже есть ключ доступа, '
                        'но я не помню, где его сохранял, требуется поиск на компьютере.',
                        'У меня уже есть ключ доступа, хотел бы записать его в файл и приступить к конвертации.',
                        'У меня уже есть ключ доступа, хочу сразу приступить к конвертации.',
                        'У меня нет ключа доступа.']
        for index, item in enumerate(first_unswer, 1):
            print(f'{index} - {item}')
        choose = int(input('\nВыберите вариант и введите соответствующее число: ').lower().strip())

        # Если пользователь выбрал в меню 1:
        if choose == 1:
            pretty_path = actual_file()
            if len(pretty_path) == 0:
                print(f'\nФайл с ключом доступа не найден.\n'
                      f'Выберите другой вариант:\n')
                continue
            else:
                for pretty_item in pretty_path:
                    str(pretty_item)
                print(f'Итак, файл с ключом доступа располагается здесь: {pretty_item}.\n')
                string_key_first = input('Используем ключ доступа из него? Введите Y/N: ').upper().strip()
                if string_key_first == 'Y':
                    empty_key.append(key_writer(pretty_path))
                else:
                    print('Выберите другой вариант:\n')
                    continue
                unswer = input('Хотите приступить к конвертации? Введите Y/N: ').upper().strip()
                if unswer == 'Y':
                    break
                else:
                    print('Выберите другой вариант:\n')
                    continue

        # Если пользователь выбрал в меню 2:
        elif choose == 2:
            # Проверка ключа доступа:
            while True:
                choose_key_second = input('\nВведите ключ доступа (Your API Key): ').lower().strip()
                if verify_key(choose_key_second) == 'False':
                    continue
                else:
                    break
            # После прохождения проверки, ключ доступа передается для записи в новосозданный файл
            print(f'Файл с ключом доступа {choose_key_second} создан в папке {new_file_creator(choose_key_second)}')
            empty_key.append(choose_key_second)
            unswer = input('Хотите приступить к конвертации? Введите Y/N: ').upper().strip()
            if unswer == 'Y':
                empty_key.append(choose_key_second)
                break
            else:
                print('Выберите другой вариант:\n')
                continue

        # Если пользователь выбрал в меню 3:
        elif choose == 3:
            # Проверка ключа доступа:
            while True:
                choose_key_third = input('\nВведите ключ доступа (Your API Key): ').lower().strip()
                if verify_key(choose_key_third) == 'False':
                    continue
                else:
                    break
            # Если ключ прошел проверку, записываем его в empty_key:
            empty_key.append(choose_key_third)
            break

        # Если пользователь выбрал в меню 4:
        elif choose == 4:
            print(f'\nВам надо пройти регистрацию по ссылке: {SITE} и получить ключ доступа')
            # Проверка ключа доступа:
            while True:
                choose_key_fourth = input('Введите ключ доступа (Your API Key): ').lower().strip()
                if verify_key(choose_key_fourth) == 'False':
                    continue
                else:
                    break
            # Если ключ прошел проверку, то передаем его дальше
            string_key_first = input(
                '\nХотите записать ключ доступа в файл, чтобы не забыть? Введите Y/N: ').upper().strip()
            if string_key_first == 'Y':
                new_file_creator(choose_key_fourth)
                empty_key.append(choose_key_fourth)
                break
            else:
                input_ = input('\nЕсли вы уже сохранили пароль в файле key_access.txt,'
                               'то запустите поиск файла\nЗапускаем поиск файла key_access.txt? Введите Y/N: ').upper().strip()
                if input_ == 'Y':
                    pretty_path = actual_file()
                    if len(pretty_path) == 0:
                        print(f'\nФайл с ключом доступа не найден.\n'
                              f'Выберите другой вариант:\n')
                        continue
                    else:
                        for pretty_item in pretty_path:
                            str(pretty_item)
                        print(f'Итак, файл с ключом доступа располагается здесь: {pretty_item}.\n')
                        string_key_first = input('Используем ключ доступа из него? Введите Y/N: ').upper().strip()
                        if string_key_first == 'Y':
                            empty_key.append(key_writer(pretty_path))
                            break
                        else:
                            print('Выберите другой вариант:\n')
                            continue
                else:
                    unswer = input('Хотите приступить к конвертации? Введите Y/N: ').upper().strip()
                    if unswer == 'Y':
                        empty_key.append(choose_key_fourth)
                        break
                    else:
                        print('Выберите другой вариант:\n')
                        continue
    return empty_key
def currency_json() -> str:
    """
    Функция хранит допустимые коды валют в json формате, на случай отсутствия файла currency.json,
    чтобы создать файл currency.json и записать допустимые коды валют в файл
    :return: допустимые коды валют в json формате
    """
    data_ = {"валюты":
                     [{"код": "EUR", "название": "Евро", "страна": "Еврозона"},
                      {"код": "USD", "название": "Доллар США", "страна": "США"},
                      {"код": "JPY", "название": "Японская иена", "страна": "Япония"},
                      {"код": "GBP", "название": "Фунт стерлингов", "страна": "Великобритания"},
                      {"код": "AUD", "название": "Австралийский доллар", "страна": "Австралия"},
                      {"код": "CAD", "название": "Канадский доллар", "страна": "Канада"},
                      {"код": "CHF", "название": "Швейцарский франк", "страна": "Швейцария"},
                      {"код": "CNY", "название": "Китайский юань", "страна": "Китай"},
                      {"код": "SEK", "название": "Шведская крона", "страна": "Швеция"},
                      {"код": "NZD", "название": "Новозеландский доллар", "страна": "Новая Зеландия"},
                      {"код": "MXN", "название": "Мексиканское песо", "страна": "Мексика"},
                      {"код": "SGD", "название": "Сингапурский доллар", "страна": "Сингапур"},
                      {"код": "HKD", "название": "Гонконгский доллар", "страна": "Гонконг"},
                      {"код": "NOK", "название": "Норвежская крона", "страна": "Норвегия"},
                      {"код": "KRW", "название": "Южнокорейская вона", "страна": "Южная Корея"},
                      {"код": "TRY", "название": "Турецкая лира", "страна": "Турция"},
                      {"код": "INR", "название": "Индийская рупия", "страна": "Индия"},
                      {"код": "RUB", "название": "Российский рубль", "страна": "Россия"},
                      {"код": "BRL", "название": "Бразильский реал", "страна": "Бразилия"},
                      {"код": "ZAR", "название": "Южноафриканский рэнд", "страна": "Южная Африка"}]
                 }
    data_json = json.dumps(data_, indent=4, ensure_ascii=False)
    return data_json

def request_base(password, base_currency) -> str:
    """
    Функция возвращает словарь курсов валют относительно введенной исходной валюты,по запросу
    на заданный сайт с курсами валют.
    :param password: код доступа полученный от пользователя
    :return: словарь курсов валют относительно введенной исходной валюты
    """
    key = password
    base_currency = base_currency
    url = f"https://v6.exchangerate-api.com/v6/{key}/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()
    return data

def verify_key(password) -> str:
    """
    Функция проверяет введенный код доступа. Код доступа должен быть получен с сайта.
    :param password: введеный код доступа
    :return: возвращает False в строковом формате, если введен неверный код доступа, и True в строковом формате,
    если введен корректный код доступа с сайта
    """
    key = password
    url = f"https://v6.exchangerate-api.com/v6/{key}/latest/USD"
    response = requests.get(url)
    str_response = str(response)
    if str_response == '<Response [403]>':
        print('Недопустимый ключ доступа! Проверьте ключ доступа!')
        result = str(False)
    else:
        result = str(True)
    return result

def request_aim(dict_base,currency_aim) -> str:
    """
    Функция считывает валюты по ключу conversion_rates в json строке, полученной с сайта по запросу
    :param dict_base:
    :param currency_aim:
    :return:
    """
    conversion_rates = dict_base['conversion_rates']
    aim_value = conversion_rates[currency_aim]
    return aim_value

def data_json() -> str:
    """
    Функция создает файл currency.json в текущей папке программы, если его там нет.
    Если файл currency.json есть или заново создается, то
    функция считывает из него словарь json и преобразует в словарь для работы в Python
    :return: список словарей для работы в Python
    """
    filepath = os.getcwd()
    new_filepath = f'{filepath}' + '\\currency.json'
    if not os.path.exists(f'{new_filepath}'):
        with open(new_filepath, 'w', encoding='utf-8') as file_1:
            file_1.write(currency_json())
        with open(new_filepath, 'r', encoding='utf-8') as file_2:
            load_from_file = json.load(file_2)
    else:
        with open(new_filepath, 'r', encoding='utf-8') as file_3:
            load_from_file = json.load(file_3)
    return load_from_file

def currency_intersection(dict_from_json) -> list[str]:
    """
    Функция анализирует
    :param dict_from_json:
    :return:
    """
    list_currency = dict_from_json['валюты']
    code_list = [dicts['код'] for dicts in list_currency]
    return code_list

def currency_name(dict_from_json):
    list_currency = dict_from_json['валюты']
    name_list = [dicts['название'] for dicts in list_currency]
    return name_list

def base_currency_verification():
    while True:
        base_currency = input('\nВведите код исходной валюты: ').upper().strip()
        dict_from_json = data_json()
        intersection = currency_intersection(dict_from_json)
        name_of_currency = currency_name(dict_from_json)
        if base_currency in intersection:
            true_base_currency = base_currency
            break
        else:
            print('\nКод исходной валюты не найден!\n'
                  'Выберите и введите допустимую валюту! Вот список допустимых валют:\n')
            for item in zip(intersection, name_of_currency):
                print(f'{item}')
            continue
    return true_base_currency

def aim_currency_verification():
    while True:
        aim_currency = input('\nВведите код целевой валюты: ').upper().strip()
        dict_from_json = data_json()
        intersection = currency_intersection(dict_from_json)
        name_of_currency = currency_name(dict_from_json)
        if aim_currency in intersection:
            true_aim_currency = aim_currency
            break
        else:
            print('\nКод целевой валюты не найден!\n'
                  'Выберите и введите допустимую валюту! Вот список допустимых валют:\n')
            for item in zip(intersection, name_of_currency):
                print(f'{item}')
            continue
    return true_aim_currency

def sum_currency_verification() -> str:
    """
    Функция проводит валидацию введенного значения, чтобы значение было числом больше 0.
    Если пользователь ввел вместо числа строку или недопустимое значение,
    то появляется сообщение о некорректном вводе и пользователь заново должен ввести данные для расчета.
    :return: корректно введеное число
    """
    while True:
        sum_currency = input('\nВведите сумму для конвертации: ').lower().strip()
        int_sum_currency = int(sum_currency)
        set_sum_currency = set(list(sum_currency))
        int_string = set(list(string.digits))
        set_minus = list(set_sum_currency.difference(int_string))
        if (len(set_minus) == 0) and (int_sum_currency > 0):
            true_sum_currency = int_sum_currency
            break
        else:
            print('Вы ввели недопустимые символы или отрицательное число!\n'
                  'Введите положительное число, отличное от 0!')
            continue
    return true_sum_currency

def calculation_currency(sum_, relation) -> int:
    """
    Функция производит конвертацию валют
    :param sum_:
    :param relation:
    :return:
    """
    x = sum_
    y = round(relation * x, 2)
    return y

# Далее написана основная функция Конвертера валют

def converter():
    """
    Основная функция конвертера валют
    :return: -
    """
    while True:
        print('\nВас приветствует программа Конвертер валют.\n'
              'Для продолжения потребуется ключ доступа.\n\n'
              'Предлагаю выбрать, что сделать дальше:')
        empty_key = []

        # Вызываем функцию меню def menu()
        menu(empty_key)

        # В результате выполнения функции def menu(),
        # преобразуем список с кодом доступа в строку для удобства работы функции request

        for keys in empty_key:
            if keys:
                key = str(keys)

        # Ввод исходной валюты и проверка есть ли такая валюта среди допустимого кода из файла currency.json
        true_currency_base = base_currency_verification()

        # Ввод целевой валюты и проверка есть ли такая валюта среди допустимого кода из файла currency.json
        true_currency_aim = aim_currency_verification()

        # После верификации вводов исходной и целевых валют, совершаем запрос на SITE и получаем словарь
        # курсов валют относительно исходной валюты
        dict_from_site_base = request_base(key, true_currency_base)

        # Получаем число соотношения курсов
        dict_from_site_aim = request_aim(dict_from_site_base, true_currency_aim)

        # Ввод суммы для конвертации и валидация введенного значения
        sum_currency = sum_currency_verification()

        # Производим конвертацию
        x = calculation_currency(sum_currency, dict_from_site_aim)
        print(f'\nЗа {sum_currency} {true_currency_base} получите {x} {true_currency_aim}')

        new_game = input('\nНачнем заново? Введите Y/N: ').upper().strip()
        if new_game == 'Y':
            continue
        else:
            print('До свидания! Хорошего дня!')
            break

if __name__ == '__main__':
    # TODO запустите здесь все необходимые функции
    converter()


