from datetime import datetime as dt
from random import randint

from access_control import access_control
from constants import ADMIN_USERNAME, UNKNOWN_COMMAND


class GuessNumber:
    def __init__(self):
        self.__start_time = dt.now()
        self.__total_games = 0
        self.__number = randint(1, 100)
        self.__username = self.__get_username()

    def __get_username(self) -> str:
        username = input('Представьтесь, пожалуйста, как Вас зовут?\n').strip()
        if username == ADMIN_USERNAME:
            print(
                '\nДобро пожаловать, создатель! '
                'Во время игры вам доступны команды "stat", "answer"'
            )
        else:
            print(f'\n{username}, добро пожаловать в игру!')
        return username

    @access_control
    def __get_statistics(self, *args, **kwargs) -> None:
        game_time = dt.now() - self.__start_time
        print(f'Общее время игры: {game_time}, текущая игра'
              '- №{self.__total_games}')

    @access_control
    def __get_right_answer(self, *args, **kwargs) -> None:
        print(f'Правильный ответ: {self.__number}')

    def __check_number(self, guess: int) -> bool:
        # Если число угадано...
        if guess == self.__number:
            print(f'Отличная интуиция, {self.__username}! '
                  'Вы угадали число :)')
            # ...возвращаем True
            return True

        if guess < self.__number:
            print('Ваше число меньше того, что загадано.')
        else:
            print('Ваше число больше того, что загадано.')
        return False

    def __game(self) -> None:
        # Получаем случайное число в диапазоне от 1 до 100.
        print(
            '\nУгадайте число от 1 до 100.\n'
            'Для выхода из текущей игры введите команду "stop"'
        )
        while True:
            # Получаем пользовательский ввод,
            # отрезаем лишние пробелы и переводим в нижний регистр.
            user_input = input('Введите число или команду: ').strip().lower()

            match user_input:
                case 'stop':
                    break
                case 'stat':
                    self.__get_statistics(username=self.__username)
                case 'answer':
                    self.__get_right_answer(username=self.__username)
                case _:
                    try:
                        guess = int(user_input)
                    except ValueError:
                        print(UNKNOWN_COMMAND)
                        continue
                    if self.__check_number(guess):
                        break

    def start(self) -> None:
        # Счётчик игр в текуsщей сессии.
        while True:
            self.__total_games += 1
            self.__game()
            play_again = input('\nХотите сыграть ещё? (yes/no) ')
            if play_again.strip().lower() not in ('y', 'yes'):
                break


if __name__ == '__main__':
    print(
        'Вас приветствует игра "Угадай число"!\n'
        'Для выхода нажмите Ctrl+C'
    )
    GuessNumber().start()
