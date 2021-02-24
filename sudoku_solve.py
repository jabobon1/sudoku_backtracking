import numpy as np
from typing import Tuple, List


def check_lines(num: int, pos: Tuple[int, int], puzzle: np.ndarray):
    """
    Проверка вертикальной и горизонтальной линии на уникальность значения
    :param pos: tuple, (y,x)
    :return: bool, True если вертикально и горизонтально такой цифры нет
    """
    num_in_vertical = np.isin(num, puzzle[pos[0]:pos[0] + 1, :])
    num_in_horizontal = np.isin(num, puzzle[:, pos[1]:pos[1] + 1])
    return not num_in_horizontal and not num_in_vertical


def check_square(num: int, pos: Tuple[int, int], puzzle: np.ndarray):
    """
    Проверка квадрата на уникальность значения
    :param pos: tuple, (y,x)
    :return: bool, True если в квадрате 3 на 3 такой цифры нет
    """
    y_st, x_st = (pos[0] // 3) * 3, (pos[1] // 3) * 3
    return not np.isin(num, puzzle[y_st:y_st + 3, x_st:x_st + 3])


def find_free(puzzle: np.ndarray) -> List[Tuple[int, int]]:
    """
    Поиск индексов ячеек с нулями
    :param puzzle: np.array, shape=(9,9)
    :return: List[(y,x)], список индексов всех пустых ячеек
    """
    free = np.where(puzzle == 0)
    return [(y, x) for y, x in zip(*free)]


def backtrack_solve(positions: List[Tuple[int, int]],
                    puzzle: np.ndarray):
    """
    Решение судоку с бэктрекингом
    :return: bool, True если решение найдено
    """
    # если свободных ячеек не осталось - значит решение найдено
    if not positions:
        return True
    # выбираем первую свободную ячейку
    pos = positions[0]
    # итеративно пытаемся подставить все возможные числа в клетку
    for num in range(1, 10):
        if check_lines(num, pos, puzzle) and check_square(num, pos, puzzle):
            # если цифра подходит для текущей ячейки, меняем ее значение и вызывыем
            # рекурсивно функцию для подстановки чисел в следующую свободную ячейку
            puzzle[pos] = num
            if backtrack_solve(positions[1:], puzzle):
                return True
            # если в каком-то рекурсивном вызове значение подобрать не удалось - сохраняем 0
            puzzle[pos] = 0
    # если ни одно число не подходит возвращаем False
    return False


def sudoku_main(puzzle: np.ndarray):
    """Главня функция для решения судоку"""
    free_pos = find_free(puzzle)
    solved = backtrack_solve(free_pos, puzzle)
    return puzzle, solved


if __name__ == '__main__':
    puzzle = np.array([[5, 3, 0, 0, 7, 0, 0, 0, 0],
                       [6, 0, 0, 1, 9, 5, 0, 0, 0],
                       [0, 9, 8, 0, 0, 0, 0, 6, 0],
                       [8, 0, 0, 0, 6, 0, 0, 0, 3],
                       [4, 0, 0, 8, 0, 3, 0, 0, 1],
                       [7, 0, 0, 0, 2, 0, 0, 0, 6],
                       [0, 6, 0, 0, 0, 0, 2, 8, 0],
                       [0, 0, 0, 4, 1, 9, 0, 0, 5],
                       [0, 0, 0, 0, 8, 0, 0, 7, 9]])

    new_paz = sudoku_main(puzzle)
    print(new_paz[0])
