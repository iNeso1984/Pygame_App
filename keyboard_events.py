import pygame

# Initialize pygame
pygame.init()

# Set up the display
w_width = 500
w_height = 500
screen = pygame.display.set_mode((w_width,w_height))
screen.fill("red")
pygame.display.set_caption("Handling keyboard events")

# Creating object
x = 0
y = 0
width = 50
height = 50
vel = 1

clock = pygame.time.Clock()
done = True  # Loop control variable

# Main loop
while done:  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            done = False  
            
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        y -= vel
    if keys[pygame.K_DOWN]:
         y += vel
    if keys[pygame.K_LEFT]:
                x -= vel
    if keys[pygame.K_RIGHT]:
          x += vel

    screen.fill("red")
    pygame.draw.rect(screen, "black", (x,y,width,height))
    clock.tick(60)
    pygame.display.flip() 
     
# Clean up
pygame.quit()
