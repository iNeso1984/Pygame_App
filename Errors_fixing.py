import pygame

# Initialize pygame
pygame.init()

# Set up the display
w_width = 500
w_height = 500
screen = pygame.display.set_mode((w_width, w_height))
screen.fill((255, 0, 0))  # Fill screen with red using RGB values
pygame.display.set_caption("Sharpshooter")

clock = pygame.time.Clock()

# Load images for background and character animations
bg_img = pygame.image.load("images/bg_img.jpeg")
bg_img = pygame.transform.scale(bg_img, (w_width, w_height))
walkRight = [pygame.image.load(f'soldier/{i}.png') for i in range(1, 10)]
walkLeft = [pygame.image.load(f'soldier/L{i}.png') for i in range(1, 10)]
char = pygame.image.load('soldier/standing.png')
moveLeft = [pygame.image.load(f'enemy/L{i}.png') for i in range(1, 10)]
moveRight = [pygame.image.load(f'enemy/R{i}.png') for i in range(1, 10)]
font = pygame.font.SysFont("helvetica", 30, 1, 1)
score = 0
bulletsound = pygame.mixer.Sound("sounds/Bulletsound.mp3")
hitsound = pygame.mixer.Sound("sounds/Hit.mp3")
music = pygame.mixer.music.load("sounds/music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)

class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 4
        self.is_jump = False
        self.jump_count = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.hit = pygame.Rect(self.hitbox)

    def draw(self, screen):
        if not self.standing:
            if self.left:
                screen.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                screen.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            # Reset walkCount to avoid exceeding index range
            if self.walkCount >= len(walkLeft) * 3:  # Multiply by 3 because of "// 3"
                self.walkCount = 0
        else:
            if self.right:
                screen.blit(walkRight[0], (self.x, self.y))
            else:
                screen.blit(walkLeft[0], (self.x, self.y))

        self.hitbox = (self.x, self.y, self.width, self.height)
        self.hit = pygame.Rect(self.hitbox)

    def touch(self):
        self.x = 0
        self.y = w_height - self.height
        self.is_jump = False
        self.jump_count = 10

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
        self.hitbox = (self.x + 20, self.y, self.width - 40, self.height - 4)
        self.hit = pygame.Rect(self.hitbox)
        self.health = 9
        self.visible = True

    def draw(self, screen):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= len(moveRight) * 3:
                self.walkCount = 0

            if self.vel > 0:
                screen.blit(moveRight[self.walkCount // 3], (self.x, self.y))
            else:
                screen.blit(moveLeft[self.walkCount // 3], (self.x, self.y))

            self.walkCount += 1
            self.hitbox = (self.x + 20, self.y, self.width - 40, self.height - 4)
            self.hit = pygame.Rect(self.hitbox)
            pygame.draw.rect(screen,"grey",(self.hitbox[0], self.hitbox[1]+3, 50, 10),0)
            pygame.draw.rect(screen, "green", (self.hitbox[0], self.hitbox[1] + 3, 50 * (self.health / 9), 10), 0)

    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] - self.width:
                self.x += self.vel
            else:
                self.vel = -self.vel
                self.walkCount = 0
        else:
            if self.x > self.path[0]:
                self.x += self.vel
            else:
                self.vel = -self.vel
                self.walkCount = 0

    def touch(self):
        hitsound.play()
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False

def DrawInGameloop():
    screen.blit(bg_img, (0, 0))
    soldier.draw(screen)
    text = font.render("Score : " + str(score), 1, "red")
    screen.blit(text, (0,10))
    enemy.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    pygame.display.flip()

soldier = Player(210, 435, 64, 64)
enemy = Enemy(0, w_height - 64, 64, 64, w_width)
bullets = []
shoot = 0
done = True
shoot_cooldown = 0

while done:
    clock.tick(27)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
    if enemy.visible:
        if soldier.hit.colliderect(enemy.hit):
            enemy.vel = enemy.vel * -1
            soldier.touch()

    if shoot > 0:
        shoot += 1
    if shoot > 3:
        shoot = 0

    # Decrement shoot_cooldown
    if shoot_cooldown > 0:
        shoot_cooldown -= 1

    for bullet in bullets[:]:
        # Check collision with the enemy
        if enemy.visible and bullet.y - bullet.radius < enemy.hitbox[1] + enemy.hitbox[3] and bullet.y + bullet.radius > enemy.hitbox[1]:
            if bullet.x + bullet.radius > enemy.hitbox[0] and bullet.x - bullet.radius < enemy.hitbox[0] + enemy.hitbox[2]:
                bullets.remove(bullet)
                score += 1
                enemy.touch()
        
        # Move the bullet if it's still on screen
        if 0 < bullet.x < w_width:
            bullet.x += bullet.vel
        else:
            bullets.remove(bullet)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shoot_cooldown == 0:
        bulletsound.play()
        direction = -1 if soldier.left else 1
        if len(bullets) < 5:
            bullets.append(Projectile(soldier.x + soldier.width // 2, soldier.y + soldier.height // 2, 8, (0, 0, 0), direction))
        shoot_cooldown = 10  # Cooldown frames (adjust this value as needed)

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
            neg = 1 if soldier.jump_count > 0 else -1
            soldier.y -= (soldier.jump_count ** 2) * 0.5 * neg
            soldier.jump_count -= 1
        else:
            soldier.is_jump = False
            soldier.jump_count = 10

    DrawInGameloop()

pygame.quit()
