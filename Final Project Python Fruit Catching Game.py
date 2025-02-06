import pygame 
import random
import sys

# Initialize Pygame
pygame.init()

#scoreboard
font = pygame.font.Font(None, 36)
score = 0

#load screen
width = 800
height = 600
screen = pygame.display.set_mode((width, height))

#clock
clock = pygame.time.Clock()

#color
COLOR = (0,0,0)
WHITE = (255, 255, 255)

#x,y variables
x=250
y=375

#projectile class
class Projectile:
    def __init__(self,x,y,speed, image):
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = 7
        self.image = image

    def update(self):
        self.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


#Image Loading
Background = pygame.image.load(r"C:\Users\south\OneDrive\Python Fruit Game\pixel_art.png")
Sprite = pygame.image.load(r"C:\Users\south\OneDrive\Python Fruit Game\basket.png").convert_alpha()
Scaled_Sprite = pygame.transform.scale(Sprite,(135,135))
banana = pygame.image.load(r"C:\Users\south\OneDrive\Python Fruit Game\apple.png")
scaled_banana = pygame.transform.scale(banana, (75, 75))
grape = pygame.image.load(r"C:\Users\south\OneDrive\Python Fruit Game\grape.png")
scaled_grape = pygame.transform.scale(grape,(75, 75))
peach = pygame.image.load(r"C:\Users\south\OneDrive\Python Fruit Game\peach.png")
scaled_peach = pygame.transform.scale(peach, (75, 75))

#variable for lives
lives = 3

#misc
vel = 10
userinput = pygame.key.get_pressed()

#projectile variables
fall_speed = 5
proj_radius = 10
proj_freq = 20
spawn_timer = 150
projectiles = []

sprite_rect = Scaled_Sprite.get_rect() #the sprites "hitbox"
 
# Keep window running
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
   
    # Handle spawns
    spawn_timer += 1
    if spawn_timer > 100:  # Spawns every ~8 seconds (500 frames at 60 FPS)
        random_x = random.randint(50, width - 50)
        random_fruit = random.choice([scaled_banana, scaled_grape, scaled_peach])
        projectiles.append(Projectile(random_x, 50, random.randint(3, 7), random_fruit))
        spawn_timer = 0

    
    # Update and draw projectiles
    for projectile in projectiles[:]:
        projectile.update()

        # Create a rectangle for the projectile to compare with the player's rectangle
        projectile_rect = pygame.Rect(projectile.x - projectile.radius, projectile.y - projectile.radius, projectile.radius * 2, projectile.radius * 2)

    # Check for collision with the player (sprite)
        if projectile_rect.colliderect(sprite_rect):  # If the projectile hits the player
            projectiles.remove(projectile)  # Remove the projectile
            score += 1 #add score when collision
        elif projectile.y > height:
            projectiles.remove(projectile)
            lives -= 1 #removing the lives

            #render and draw the lives text
    
    # Remove projectiles that fall off the screen
    projectiles = [p for p in projectiles if p.y < height] 


    # Draw background first
    screen.blit(Background, (0, 0))

    
    for projectile in projectiles:
        projectile.draw(screen)

    # Draw player sprite
    screen.blit(Scaled_Sprite, (x, y))
    sprite_rect.topleft = (x, y)  # Update the sprite's rectangle position

    # Player movement
    userinput = pygame.key.get_pressed()
    if userinput[pygame.K_a] and x > 0:
        x -= vel
    if userinput[pygame.K_d] and x < 662:
        x += vel

    score_text = font.render(f"score: {score}", True, COLOR)
    screen.blit(score_text,(15,15))

    lives_text = font.render("lives: " + str(lives), True, (255, 0, 0))
    screen.blit(lives_text,(15,50))

    if lives == 0:
        pygame.quit()
        sys.exit()


    pygame.display.update()
    clock.tick(60)

pygame.quit()