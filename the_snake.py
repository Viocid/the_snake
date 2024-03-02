from random import randint

import pygame as pg

import sys

# Инициализация PyGame:
pg.init()

# Аннотации типов
COLOR = tuple[int, int, int]
T_INT = tuple[int, int]

# Константы для размеров поля и сетки:
SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP: T_INT = (0, -1)
DOWN: T_INT = (0, 1)
LEFT: T_INT = (-1, 0)
RIGHT: T_INT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR: COLOR = (255, 255, 255)

# Цвет границы ячейки
BORDER_COLOR: COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR: COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR: COLOR = (0, 255, 0)

# Цвет по умолчанию
B_COLOR: COLOR = (0, 0, 0)

# Скорость движения змейки:
SPEED: int = 20

# Центр экрана
CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Поправка
AMENDMENT = 20
# Настройка игрового окна:
screen = pg.display.set_mode((
    SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Основной класс игры."""

    def __init__(self, body_color=B_COLOR):
        """Базовые атрибуды.
        Определяет центральную точку экрана, цвет объекта.
        """
        self.position = CENTER
        self.body_color = body_color

    def draw(self):
        """Необходим для дочерних классов."""
        raise NotImplementedError('Необходим для дочерних классов.')


class Snake(GameObject):
    """Класс определяющий змейку."""

    max_length = 0

    def __init__(self, body_color=SNAKE_COLOR):
        """Определяет длинну змейки, позицию, напраление движения,
        следующее направление движения, цвет змейки.
        """
        super().__init__()
        self.body_color = body_color
        self.positions = [CENTER]
        self.length = len(self.positions)
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Оновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращаяет координаты головы змейки."""
        return (self.positions[0])

    def move(self):
        """Обновляет позицию змейки, добовляя новую голову."""
        head = self.get_head_position()
        x = (self.direction[0]) * GRID_SIZE + (head[0])
        y = (self.direction[1]) * GRID_SIZE + (head[1])
        head_1 = ()
        if int(x) >= int(SCREEN_WIDTH):
            head_1 = 0, y
        elif int(y) >= int(SCREEN_HEIGHT):
            head_1 = x, 0
        elif int(x) < 0:
            head_1 = (SCREEN_WIDTH - AMENDMENT), y
        elif int(y) < 0:
            head_1 = x, (SCREEN_HEIGHT - AMENDMENT)
        else:
            head_1 = x, y

        new_position = head_1

        self.positions.insert(0, new_position)

    def draw(self, surface):
        """Отрисовывает змейку на экране и затирает след."""
        for position in self.positions[:-1]:
            rect = (
                pg.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pg.draw.rect(surface, self.body_color, rect)
            pg.draw.rect(surface, BORDER_COLOR, rect, 1)
        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(surface, self.body_color, head_rect)
        pg.draw.rect(surface, BORDER_COLOR, head_rect, 1)
        if self.last:
            last_rect = pg.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pg.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Сбрасывает змейку."""
        if len(self.positions) > self.max_length:
            self.max_length = len(self.positions)
        max = self.max_length
        self.length = 1
        self.positions = [CENTER]
        pg.display.set_caption(f'Змейка Cкорость змейки {sn_speed} '
                               f'Рекордная длина {max}'
                               )


class Apple(Snake):
    """Класс яблока."""

    def __init__(self):
        """Задает цвет яблока,
        вызывает метод устанавливающий начальную позицию яблока.
        """
        super().__init__()
        snake = self.positions
        self.body_color = APPLE_COLOR
        self.randomize_position(snake)

    def randomize_position(self, snake):
        """Устанавливает случайное положение яблока на игровом поле."""
        while True:
            new_position = (
                randint(0, GRID_WIDTH) * GRID_SIZE,
                randint(0, GRID_HEIGHT) * GRID_SIZE
            )
            if ((SCREEN_WIDTH - AMENDMENT) < new_position[0]
                or new_position[0] < 0
                or (SCREEN_HEIGHT - AMENDMENT) < new_position[1]
                or new_position[1] < 0
                    or new_position in snake):

                new_position = (
                    randint(0, GRID_WIDTH) * GRID_SIZE,
                    randint(0, GRID_HEIGHT) * GRID_SIZE
                )
            else:
                self.position = new_position
                break

    def draw(self, surface):
        """Отрисовывает яблоко."""
        rect = pg.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pg.draw.rect(surface, self.body_color, rect)
        pg.draw.rect(surface, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Обрабатывает нажатие клавиш."""
    events = {
        (LEFT, pg.K_UP): UP,
        (RIGHT, pg.K_UP): UP,
        (DOWN, pg.K_LEFT): LEFT,
        (UP, pg.K_LEFT): LEFT,
        (LEFT, pg.K_DOWN): DOWN,
        (RIGHT, pg.K_DOWN): DOWN,
        (UP, pg.K_RIGHT): RIGHT,
        (DOWN, pg.K_RIGHT): RIGHT
    }

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            game_object.next_direction = events.get(
                (game_object.direction, event.key)
            )


def main():
    """Основной цикл игры. Обрабатывает нажатие клавиш, двигает змейку,
    обновляет направление движения змейки,
    проверяет съела ли яблоко змейка и не столкнулась ли она с собой,
    отрисовывает змейку и яблоко, обновляет экран.
    """
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()
    screen.fill(BOARD_BACKGROUND_COLOR)
    while True:
        clock.tick(SPEED)
        # Тут опишите основную логику игры.
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        head = snake.get_head_position()
        snake_1 = snake.positions
        if head in snake.positions[2:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        else:
            if snake.get_head_position() == apple.position:
                apple.randomize_position(snake_1)
            else:
                snake.last = snake.positions.pop()

        apple.draw(screen)
        snake.draw(screen)
        pg.display.update()


# Заголовок окна игрового поля:
snake = Snake()
max = snake.max_length
sn_speed = str(SPEED)
pg.display.set_caption(f'Змейка Cкорость змейки {sn_speed} '
                       f'Рекордная длина {max}')

"""Запуск игры."""
if __name__ == '__main__':
    main()
