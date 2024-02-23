from random import choice, randint

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
SPEED = 5

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH + 20, SCREEN_HEIGHT + 20), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:

    def __init__(self, body_color=(0, 0, 0)):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def draw(self):
        pass


class Snake(GameObject):
    
    def __init__(self, direction=choice([UP, DOWN, LEFT, RIGHT])):
        super().__init__(body_color=SNAKE_COLOR)
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.length = len(self.positions)
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        return (self.positions[0])

    def move(self):
        head = self.get_head_position()
        x = (self.direction[0]) * GRID_SIZE + (head[0])
        y = (self.direction[1]) * GRID_SIZE + (head[1])
        head_1 = ()
        if int(x) > int(SCREEN_WIDTH):
            head_1 = 0, y
        elif int(y) > int(SCREEN_HEIGHT):
            head_1 = x, 0
        elif int(x) < 0:
            head_1 = SCREEN_WIDTH, y
        elif int(y) < 0:
            head_1 = x, SCREEN_HEIGHT
        else:
            head_1 = x, y
        
        new_position = head_1

        self.positions.insert(0, new_position)

    def draw(self, surface):
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
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        screen.fill(BOARD_BACKGROUND_COLOR)
        
def handle_keys(game_object):
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

class Apple(GameObject):

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()
        if SCREEN_WIDTH < self.position[0] < 0 and SCREEN_HEIGHT < self.position[1] < 0:
            self.randomize_position()

    def randomize_position(self):
        self.position = (
            randint(0, GRID_WIDTH) * GRID_SIZE,
            randint(0, GRID_HEIGHT) * GRID_SIZE
        )

    def draw(self, surface):
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

def main():
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()
    screen.fill(BOARD_BACKGROUND_COLOR)
    while True:
        clock.tick(SPEED)
        # Тут опишите основную логику игры.
        handle_keys(snake)
        snake.update_direction()
        new_position = snake.move()
        if new_position in snake.positions[2:]:
            snake.reset()
            
        else:
            if snake.get_head_position() == apple.position:
                apple.randomize_position()
            else:
                snake.last = snake.positions.pop()

        apple.draw(screen)
        snake.draw(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        pygame.display.update()

def update_direction(self):
    if self.next_direction:
        self.direction = self.next_direction
        self.next_direction = None

if __name__ == '__main__':
    main()
