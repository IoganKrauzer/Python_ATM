"""Задача 5
Напишите программу банкомат.
✔ Начальная сумма равна нулю
✔ Допустимые действия: пополнить, снять, выйти
✔ Сумма пополнения и снятия кратны 50 у.е.
✔ Процент за снятие — 1.5% от суммы снятия, но не менее 30 и не более 600 у.е.
✔ После каждой третей операции пополнения или снятия начисляются проценты - 3%
✔ Нельзя снять больше, чем на счёте
✔ При превышении суммы в 5 млн, вычитать налог на богатство 10% перед каждой
операцией, даже ошибочной
✔ Любое действие выводит сумму денег"""

import os
os.system('cls')


# Функция для вступительного сообщения
def show_welcome_message(message):
    print('-----------------------------------------------------------')
    print(message)


# Показать опции банкомата
def show_atm_options():
    print('-----------------------------------------------------------')
    print('Банкомат "Фури-Кури" предоставляет следующие операции:')
    print('-----------------------------------------------------------')
    print('|\t1# Баланс\t\t\t\t|')
    print('|\t2# Пополнить баланс\t\t|')
    print('|\t3# Снять деньги\t\t\t|')
    print('|\t4# Повторить операции\t|')
    print('|\t5# Счётчик операций\t\t|')
    print('|\t0# Выход\t\t\t\t|')
    print('-----------------------------------------------------------')


# Чем заменить табуляцию ? --------------------------------------------------------------------------------------------

# Начисление процента за каждую 3-ю операцию
def plus_percent_for_every_3_operations():
    global atm_cash
    print(f'Каждая 3-я операция начисляет {PERCENT_FOR_EVERY_3_OPERATION} % к вашему счету ' +
          f'Текущее начисление составило: {digits_numbers((atm_cash / 100) * PERCENT_FOR_EVERY_3_OPERATION)} y.e.')
    atm_cash += ((atm_cash / 100) * PERCENT_FOR_EVERY_3_OPERATION)
    print(f'Ваш баланс составляет: {digits_numbers(atm_cash)} y.e.')


# Проверка и вычисление процента на богатство
def wealth_tax_operation():
    global atm_cash
    if atm_cash >= MAX_WEALTH_TAX_SUM:
        helper_for_wealth_tax = (atm_cash / 100) * WEALTH_TAX
        atm_cash -= (atm_cash / 100) * WEALTH_TAX
        print(f'Налог на богатство составил: {digits_numbers(helper_for_wealth_tax)} ' +
              f'Ваш баланс составляет: {digits_numbers(atm_cash)} y.e.')


# Для внешнего вида разрядности чисел
def digits_numbers(number):
    number = '{0:,}'.format(number).replace(',', ' ')
    return number


# Для вызова соответствующих функций для каждой команды + проверка счетчика + вызов функции налога на богатство
def processing_options(_user_choice):
    global atm_cash
    global atm_operation_counter

    if user_choice == 1:
        print(f'Ваш баланс составляет: {digits_numbers(atm_cash)} y.e.')
    elif user_choice == 4:
        show_atm_options()
    elif user_choice == 5:
        print(f'Учитываются только операции положить / снять деньги! \n\tТекущий счётчик: {atm_operation_counter}')
    elif user_choice in atm_operation_number_list[: len(atm_operation_number_list):]:
        if user_choice == 2:
            deposit_cash_in()
        elif user_choice == 3:
            withdraw_cash()
        atm_operation_counter += 1
    if atm_operation_counter % 3 == 0 and atm_operation_counter != 0:
        plus_percent_for_every_3_operations()
    wealth_tax_operation()


# Проверка на номер операции
def user_choice_checker(_user_choice):
    _user_choice_checker = True
    result = True
    while _user_choice_checker:
        if _user_choice in atm_operation_number_list and _user_choice != 0:
            result = True
            _user_choice_checker = False
        elif _user_choice == 0:
            result = False
            _user_choice_checker = False
        else:
            print('Такой операции не существует')
            _user_choice = user_choice_operation()
    return result


# Пополнение наличными
def deposit_cash_in():
    deposit_cash_checker = True
    global atm_cash
    print('На какую сумму вы хотите пополнить? Допустимая сумма пополнения не может быть отрицательной' +
          ' и должна быть кратна 50 y.e.')
    while deposit_cash_checker:
        print('-----------------------------------------------------------')
        user_deposit_cash = int(input('Введите сумму пополнения в y.e.: '))
        print('-----------------------------------------------------------')
        if user_deposit_cash % 50 or user_deposit_cash < 0:
            if user_deposit_cash % 50:
                print('Сумма пополнения должна быть кратна 50 y.e.')
                continue
            elif user_deposit_cash < 0:
                print('Введенная сумма не может быть отрицательной')
                continue
        else:
            atm_cash += user_deposit_cash
            print(f'Ваш баланс составляет: {digits_numbers(atm_cash)} y.e.')
            deposit_cash_checker = False


# Для расчета комиссии на сумму для снятия
def percentage_operation(user_withdraw_cash):
    if (user_withdraw_cash / 100) * ATM_WITHDRAW_COMMISSION <= MIN_LIMIT_COMMISSION:
        return MIN_LIMIT_COMMISSION
    elif MIN_LIMIT_COMMISSION < (user_withdraw_cash / 100) * ATM_WITHDRAW_COMMISSION < MAX_LIMIT_COMMISSION:
        return (user_withdraw_cash / 100) * ATM_WITHDRAW_COMMISSION
    elif (user_withdraw_cash / 100) * ATM_WITHDRAW_COMMISSION >= MAX_LIMIT_COMMISSION:
        return MAX_LIMIT_COMMISSION


# Для выявления минимальной суммы для снятия денег
def min_cash_for_withdraw(user_withdraw_cash):
    global atm_cash
    sum_for_min_limit_commission = int(100 * (MIN_LIMIT_COMMISSION / ATM_WITHDRAW_COMMISSION))
    sum_for_max_limit_commission = int(100 * (MAX_LIMIT_COMMISSION / ATM_WITHDRAW_COMMISSION))
    if user_withdraw_cash <= sum_for_min_limit_commission:
        print(f'Максимальная сумма доступная для снятия: {atm_cash - MIN_LIMIT_COMMISSION} y.e.')
    elif user_withdraw_cash >= sum_for_max_limit_commission:
        print(f'Максимальная сумма доступная для снятия: {atm_cash - MAX_LIMIT_COMMISSION} y.e.')
    else:
        _helper_for_count_operation = sum_for_min_limit_commission
        counter_helper = sum_for_min_limit_commission
        while True:
            counter_helper += 10
            if counter_helper + ((counter_helper / 100) * ATM_WITHDRAW_COMMISSION) > atm_cash:
                break
            _helper_for_count_operation = counter_helper + ((counter_helper / 100) * ATM_WITHDRAW_COMMISSION)

        print(f'Максимальная сумма доступная для снятия: {digits_numbers(_helper_for_count_operation)} y.e.')


# Для снятия денег с банкомата
def withdraw_cash():
    withdraw_cash_checker = True
    global atm_cash
    print('-----------------------------------------------------------')
    print(f'Минимальная комиссия: {MIN_LIMIT_COMMISSION} y.e.' +
          f'| Максимальная комиссия: {MAX_LIMIT_COMMISSION} y.e.' +
          f'\nКомиссия составляет: {ATM_WITHDRAW_COMMISSION} % ')
    print('-----------------------------------------------------------')
    while withdraw_cash_checker:
        user_withdraw_cash = int(input('Какую сумму вы хотите снять?: '))
        if atm_cash < user_withdraw_cash + percentage_operation(user_withdraw_cash):
            print(f'Запрашиваемая сумма превышает ваш баланс! Ваш баланс: {atm_cash} y.e.')
            print('Введите другую сумму! Учтите - сумма должна включать комиссию 1.5%')
            min_cash_for_withdraw(user_withdraw_cash)
            continue
        else:
            atm_cash -= user_withdraw_cash + percentage_operation(user_withdraw_cash)
            print(
                f'Ваш баланс составляет: {digits_numbers(atm_cash)} y.e. ' +
                f'Комиссия составила: {percentage_operation(user_withdraw_cash)} y.e.')
            withdraw_cash_checker = False


# Для запроса номера операции
def user_choice_operation():
    print('-----------------------------------------------------------')
    user_choice_number = int(input('Введите номер операции: '))
    print('-----------------------------------------------------------')
    return user_choice_number


# atm => банкомат
ATM_WITHDRAW_COMMISSION = 1.5
MIN_LIMIT_COMMISSION = 30
MAX_LIMIT_COMMISSION = 600
MIN_CASH_WITHDRAW = 100
PERCENT_FOR_EVERY_3_OPERATION = 3
WEALTH_TAX = 10
MAX_WEALTH_TAX_SUM = 5_000_000
atm_cash = 2500
atm_operation_counter = 2
atm_operation_number_list = [1, 2, 3, 4, 5, 0]
welcome_message = 'Вас приветствует банкомат компании "Фури-Кури"'
atm_status = True

show_welcome_message(welcome_message)
show_atm_options()

while atm_status:
    user_choice = user_choice_operation()
    atm_status = user_choice_checker(user_choice)
    if atm_status:
        processing_options(user_choice)
    else:
        print('Спасибо что воспользовались услугами банкомата "Фури-Кури"')
        print('-----------------------------------------------------------')
        atm_status = False
