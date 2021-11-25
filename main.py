#sprite
import pygame
import random

FPS = 60
WIDTH = 500
HEIGHT = 500

BLACK = (0, 0, 0)
WHITE = (255,255,255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

#Game initialization and creating Windows
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Game")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
  def __init__(self):
      pygame.sprite.Sprite.__init__(self)
      self.image = pygame.Surface((50, 40))
      self.image.fill(GREEN)
      self.rect = self.image.get_rect()
      self.rect.centerx = WIDTH / 2
      self.rect.bottom = HEIGHT - 10
      self.speedx = 8

  def update(self):
      key_pressed = pygame.key.get_pressed()
      if key_pressed[pygame.K_d]:
        self.rect.x += self.speedx
      if key_pressed[pygame.K_a]:
        self.rect.x -= self.speedx 

      if self.rect.right > WIDTH:
        self.rect.right = WIDTH
      if self.rect.left < 0:
        self.rect.left = 0

  def shoot(self):
      bullet = Bullet(self.rect.centerx, self.rect.top)
      all_sprites.add(bullet)
      bullets.add(bullet)


class Rock(pygame.sprite.Sprite):
  def __init__(self):
      pygame.sprite.Sprite.__init__(self)
      self.image = pygame.Surface((30, 40))
      self.image.fill(RED)
      self.rect = self.image.get_rect()
      self.rect.x = random.randrange(0, WIDTH - self.rect.width)
      self.rect.y = random.randrange(-100, -40) 
      self.speedy = random.randrange(2, 10)
      self.speedx = random.randrange(-3, 3)

  def update(self):
      self.rect.y += self.speedy
      self.rect.x += self.speedx
      if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-3, 3)        

class Bullet(pygame.sprite.Sprite):
  def __init__(self, x, y):
      pygame.sprite.Sprite.__init__(self)
      self.image = pygame.Surface((10, 20))
      self.image.fill(YELLOW)
      self.rect = self.image.get_rect()
      self.rect.centerx = x
      self.rect.bottom = y
      self.speedy = -10
      

  def update(self):
      self.rect.y += self.speedy
      if self.rect.bottom < 0:
          self.kill()

all_sprites = pygame.sprite.Group()
rocks = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    r = Rock()
    all_sprites.add(r)
    rocks.add(r)

#game loop
running  = True

while running:
  clock.tick(FPS)
  #get input
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            player.shoot()

  #update game
  all_sprites.update() 
  hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
  for hit in hits:
      r = Rock()
      all_sprites.add(r)
      rocks.add(r)

  hits = pygame.sprite.spritecollide(player, rocks, False)
  if hits:
      running = False

  #display screen
  screen.fill(BLACK)
  all_sprites.draw(screen)
  pygame.display.update()

pygame.quit()