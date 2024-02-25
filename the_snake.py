from random import randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (255, 255, 255)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((
    SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Основной класс игры."""

    def __init__(self, body_color=(0, 0, 0)):
        """Базовые атрибуды.
        Определяет центральную точку экрана, цвет объекта.
        """
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def draw(self):
        """Необходим для дочерних классов."""
        pass


class Snake(GameObject):
    """Класс определяющий змейку."""

    def __init__(self):
        """Определяет длинну змейки, позицию, напраление движения,
        следующее направление движения, цвет змейки.
        """
        super().__init__(body_color=SNAKE_COLOR)
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
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
            head_1 = (SCREEN_WIDTH - 20), y
        elif int(y) < 0:
            head_1 = x, (SCREEN_HEIGHT - 20)
        else:
            head_1 = x, y

        new_position = head_1

        self.positions.insert(0, new_position)

    def draw(self, surface):
        """Отрисовывает змейку на экране и затирает след."""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Сбрасывает змейку."""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Обрабатывает нажатие клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


class Apple(Snake):
    """Класс яблока."""

    def __init__(self):
        """Задает цвет яблока,
        вызывает метод устанавливающий начальную позицию яблока.
        """
        super().__init__()
        snake = Snake().positions
        self.body_color = APPLE_COLOR
        self.randomize_position(snake)

    def randomize_position(self, snake):
        """Устанавливает случайное положение яблока на игровом поле."""
        snake = snake
        self.position = (
            randint(0, GRID_WIDTH) * GRID_SIZE,
            randint(0, GRID_HEIGHT) * GRID_SIZE
        )
        if (SCREEN_WIDTH - 20) < self.position[0]\
            or self.position[0] < 0\
            or (SCREEN_HEIGHT - 20) < self.position[1]\
            or self.position[1] < 0\
                or self.position in snake:
            self.position = (
                randint(0, GRID_WIDTH) * GRID_SIZE,
                randint(0, GRID_HEIGHT) * GRID_SIZE
            )

    def draw(self, surface):
        """Отрисовывает яблоко."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


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

        else:
            if snake.get_head_position() == apple.position:
                apple.randomize_position(snake_1)
            else:
                snake.last = snake.positions.pop()

        apple.draw(screen)
        snake.draw(screen)

        pygame.display.update()


"""Запуск игры."""
if __name__ == '__main__':
    main()
