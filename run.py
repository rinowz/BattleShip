import pygame
import random
import os

WIDTH = 1280
HEIGHT = 1084
FPS = 60

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

image = pygame.image.load('ps.png').convert_alpha()

screen.blit(image, (100, 111))

class Ship(pygame.sprite.Sprite):
    '''Основной корабль
    задается его положение, и движение, только начало, необходимо продолжить писать'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = screen.blit(image, (100, 111))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        
        
    def update(self):
        self.rect.x += 5
        if self.rect.left > WIDTH:
            self.rect.right = 0


# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ship")
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
player = Ship()
all_sprites.add(player)


# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Обновление
    all_sprites.update()
    
    # Рендеринг
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()