
def validation(first, second, operation):
    try:
        float(first)
        float(second)
        result_int = True
    except ValueError:
        result_int = False
    match operation:
        case '+':
            result = True
        case '-':
            result = True
        case '*':
            result = True
        case '/':
            result = True
        case _:
            result = False
    return result_int, result

def client_round(result, round_result):
    try:
        true_int = int(round_result)
        result_round = round(result, true_int)
        result_bool = True
    except ValueError:
        result_bool = False
        result_round = None
    return result_round, result_bool

def calculator():
    while True:
        first = input('Введите первое число: ')
        second = input('Введите второе число: ')
        operation = input('Введите операцию вычисления: ')
        result = list(validation(first, second, operation))
        if False in result:
            print('Вы ввели некорректные данные!')
            continue
        else:
            break
    first_float = float(first)
    second_float = float(second)
    match operation:
        case '+':
            result_operation = first_float + second_float
        case '-':
            result_operation = first_float - second_float
        case '*':
            result_operation = first_float * second_float
        case '/':
            try:
                if second_float == 0:
                    raise ZeroDivisionError
            except ZeroDivisionError:
                second = input('Деление на 0!\nВведите второе число: ')
                second_float = float(second)
            result_operation = first_float / second_float
    return result_operation

def main_function():
    while True:
        print('\nВас приветствует программа Калькулятор.\n\n'
              'Предлагаю выбрать, что сделать дальше:')
        client_unswer = ['Запуск калькулятора', 'Выход']
        for index, item in enumerate(client_unswer, 1):
            print(f'{index} - {item}')
        choose = int(input('\nВыберите вариант и '
                           'введите соответствующее число: ').lower().strip())
        match choose:
            case 1:
                result_of_calculation = calculator()
                while True:
                    round_result = input('До какого знака хотели бы округлить полученное число?: ')
                    result = list(client_round(result_of_calculation, round_result))
                    if False in result:
                        print('Вы ввели некорректные данные округления!')
                        continue
                    else:
                        break
                print(f'\nРезультат вычисления: {result[0]}')
            case 2:
                print('До свидания! Хорошего дня!')
                break
            case _:
                print('Выберите корректный вариант!')
                continue

if __name__ == '__main__':
    main_function()


