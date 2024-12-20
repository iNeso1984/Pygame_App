import pygame

# Initialize pygame
pygame.init()

# Set up the display
w_width = 500
w_height = 500
screen = pygame.display.set_mode((w_width, w_height))
screen.fill("red")
pygame.display.set_caption("Adding enemy")

clock = pygame.time.Clock()
bg_img = pygame.image.load("images/bg_img.jpeg")
bg_img = pygame.transform.scale(bg_img, (w_width, w_height))

# Load images for soldier and enemy animations
walkRight = [pygame.image.load(f'soldier/{i}.png') for i in range(1, 10)]
walkLeft = [pygame.image.load(f'soldier/L{i}.png') for i in range(1, 10)]
char = pygame.image.load('soldier/standing.png')
moveLeft = [pygame.image.load(f'enemy/L{i}.png') for i in range(1, 10)]
moveRight = [pygame.image.load(f'enemy/R{i}.png') for i in range(1, 10)]

class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.is_jump = False
        self.jump_count = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True

    def draw(self, screen):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not self.standing:
            if self.left:
                screen.blit(walkLeft[self.walkCount // 3], (self.x, self.y))  # Use soldier's walkLeft
                self.walkCount += 1
            elif self.right:
                screen.blit(walkRight[self.walkCount // 3], (self.x, self.y))  # Use soldier's walkRight
                self.walkCount += 1
        else:
            if self.right:
                screen.blit(walkRight[0], (self.x, self.y))
            else:
                screen.blit(walkLeft[0], (self.x, self.y))

class Projectile:
    def __init__(self, x, y, radius, color, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = direction
        self.vel = 8 * direction

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

class Enemy:
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.walkCount = 0
        self.vel = 3
        self.path = [x, end]
        self.standing = True

    def draw(self, screen):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if self.vel > 0:
            screen.blit(moveRight[self.walkCount // 3], (self.x, self.y))
        else:
            screen.blit(moveLeft[self.walkCount // 3], (self.x, self.y))
        self.walkCount += 1

    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] - self.width:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

def DrawInGameloop():
    screen.blit(bg_img, (0, 0))
    soldier.draw(screen)
    enemy.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    pygame.display.flip()

soldier = Player(50, 435, 64, 64)
enemy = Enemy(0, 410, 64, 64, w_width)
bullets = []

done = True
while done:
    clock.tick(27)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False

    for bullet in bullets:
        if 0 < bullet.x < 500:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        direction = -1 if soldier.left else 1
        if len(bullets) < 5:
            bullets.append(Projectile(soldier.x + soldier.width // 2, soldier.y + soldier.height // 2, 6, "#3b3b3b", direction))

    if keys[pygame.K_LEFT] and soldier.x > 0:
        soldier.x -= soldier.vel
        soldier.left = True
        soldier.right = False
        soldier.standing = False
    elif keys[pygame.K_RIGHT] and soldier.x < w_width - soldier.width:
        soldier.x += soldier.vel
        soldier.right = True
        soldier.left = False
        soldier.standing = False
    else:
        soldier.standing = True
        soldier.walkCount = 0

    if not soldier.is_jump:
        if keys[pygame.K_UP]:
            soldier.is_jump = True
            soldier.right = False
            soldier.left = False
    else:
        if soldier.jump_count >= -10:
            neg = 1 if soldier.jump_count >= 0 else -1
            soldier.y -= (soldier.jump_count ** 2) * neg * 0.5
            soldier.jump_count -= 1
        else:
            soldier.jump_count = 10
            soldier.is_jump = False

    enemy.move()
    DrawInGameloop()

pygame.quit()
