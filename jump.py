import pygame

# Initialize pygame
pygame.init()

# Set up the display
w_width = 500
w_height = 500
screen = pygame.display.set_mode((w_width,w_height))
screen.fill("red")
pygame.display.set_caption("Adding jump logic")

# Creating object
x = 0
y = 0
width = 50
height = 50
vel = 5

clock = pygame.time.Clock()

# Jump variables
is_jump = False
jump_count = 10

done = True  # Loop control variable

# Main loop
while done:  
     for event in pygame.event.get():
          if event.type == pygame.QUIT:  
               done = False  
            
     keys = pygame.key.get_pressed()

     if keys[pygame.K_LEFT] and x>0:
          x -= vel
     if keys[pygame.K_RIGHT] and x < w_width-width:
          x += vel

     if not(is_jump):
          if keys[pygame.K_UP] and y>0:
              y -= vel
          if keys[pygame.K_DOWN] and y < w_height-height:
              y += vel
          if keys[pygame.K_SPACE]:
              is_jump = True
     else:
          if is_jump:
               if jump_count >=-10:
                   neg = 1
                   if jump_count < 0:
                       neg = -1
                   y -= (jump_count ** 2) * neg * 0.5
                   jump_count -= 1
               else:
                   jump_count = 10
                   is_jump = False

     screen.fill("red")
     pygame.draw.rect(screen, "black", (x,y,width,height))
     clock.tick(60)
     pygame.display.flip() 
     
# Clean up
pygame.quit()
