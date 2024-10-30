import pygame

# Initialize pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((300, 300))  # Window size
screen.fill("white")  # Fill the screen with white
pygame.display.set_caption("My first pygame program")  # Window title

done = False  # Loop control variable

# Main loop
while not done:  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            done = True  


    pygame.display.flip() 
     
# Clean up
pygame.quit()
