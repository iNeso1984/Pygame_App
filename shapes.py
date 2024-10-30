import pygame

# Initialize pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((500, 500))  # Window size
screen.fill("white")  # Fill the screen with white
pygame.display.set_caption("Shapes galore")  # Window title

# Drawing two lines
pygame.draw.line(screen, "blue", (0, 0), (300, 300), 5)
pygame.draw.lines(screen, "red", True, [(100, 100), (200, 100), (100, 200)], 5)  # Fix the coordinates and drawing method
pygame.draw.rect(screen, "black", (50,50,100,100), 0)
pygame.draw.circle(screen, "green", (200,150), 50, 0)
pygame.draw.ellipse(screen, "yellow", (300, 100, 100, 50), 0)
pygame.draw.polygon(screen, "purple", ((250,75), (300,25), (350,75)), 0)

done = True  # Loop control variable

# Main loop
while done:  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            done = False  # Set done to False when window is closed

    pygame.display.flip()  # Update the display
     
# Clean up
pygame.quit()
