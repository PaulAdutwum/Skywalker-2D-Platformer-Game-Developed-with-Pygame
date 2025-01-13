import pygame
import random
import time


pygame.init()

# Screen setup
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Paul's Mario Jump Game")
clock = pygame.time.Clock()

mario_image = pygame.image.load('/Users/pauladutwum/Downloads/mario.png')


mario_image = pygame.transform.scale(mario_image, (50, 50))

mario_rect = mario_image.get_rect()
mario_rect.x = 50
mario_rect.y = SCREEN_HEIGHT - 100


collision_sound = pygame.mixer.Sound('/Users/pauladutwum/Documents/Myprojects/Equatorial Complex.mp3')


pygame.mixer.music.load('/Users/pauladutwum/Documents/Myprojects/Nowhere Land.mp3')
pygame.mixer.music.play(-1) 

# Game over font
font = pygame.font.Font(None, 72)
small_font = pygame.font.Font(None, 36)

is_jumping = False
jump_speed = 20
gravity = 1
velocity = 1
ground_level = SCREEN_HEIGHT - 150    
mario_speed = 5  


obstacle_width = 80
obstacle_height = 100
obstacle_speed = 5
obstacle_shapes = ["rect", "circle", "car", "furniture"]  
obstacle_x = SCREEN_WIDTH
obstacle_y = SCREEN_HEIGHT - obstacle_height - 50
speed_increase = 0.05  
current_shape = random.choice(obstacle_shapes)


score = 0
points_per_jump = 10
highest_score = 0


try:
    with open("highest_score.txt", "r") as file:
        highest_score = int(file.read())
except FileNotFoundError:
    highest_score = 0


background_color = (255, 255, 255)  

def reset_game():
    global is_jumping, velocity, obstacle_x, obstacle_speed, score, current_shape, background_color
    is_jumping = False
    velocity = 0
    obstacle_x = SCREEN_WIDTH
    obstacle_speed = 5
    score = 0
    current_shape = random.choice(obstacle_shapes)
    background_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # New random color
    pygame.mixer.music.play(-1)  

def countdown():
    for i in range(3, 0, -1):
        screen.fill((0, 0, 0))
        countdown_text = font.render(str(i), True, (255, 255, 255))
        screen.blit(countdown_text, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        pygame.display.update()
        time.sleep(1)
    screen.fill((0, 0, 0))
    intro_text = font.render("Go!", True, (255, 255, 255))
    screen.blit(intro_text, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    pygame.display.update()
    time.sleep(1)


def save_highest_score():
    global highest_score, score
    if score > highest_score:
        highest_score = score
        with open("highest_score.txt", "w") as file:
            file.write(str(highest_score))



def game_loop():
    global score, is_jumping, velocity, obstacle_x, highest_score, obstacle_speed, background_color, current_shape 
    running = True
    game_over = False

    countdown()  

    while running:
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                running = False

            if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game_over = False
                reset_game()

           
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not is_jumping:
                    is_jumping = True
                    velocity = -jump_speed

        if not game_over:
           
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                mario_rect.x -= mario_speed
                if mario_rect.x < 0: 
                    mario_rect.x = 0

            if keys[pygame.K_RIGHT]:
                mario_rect.x += mario_speed
                if mario_rect.x + mario_rect.width > SCREEN_WIDTH:  
                    mario_rect.x = SCREEN_WIDTH - mario_rect.width

           
            if is_jumping:
                mario_rect.y += velocity
                velocity += gravity
                if mario_rect.y >= ground_level:
                    mario_rect.y = ground_level
                    is_jumping = False

           
            obstacle_x -= obstacle_speed
            if obstacle_x < 0:
                obstacle_x = SCREEN_WIDTH
                obstacle_speed += speed_increase 
                current_shape = random.choice(obstacle_shapes) 

               
                background_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

          
            screen.fill(background_color)

            # Draw Mario
            screen.blit(mario_image, mario_rect)

           
            if current_shape == "rect":
                pygame.draw.rect(screen, (255, 0, 0), (obstacle_x, obstacle_y, obstacle_width, obstacle_height))
            elif current_shape == "circle":
                pygame.draw.circle(screen, (0, 0, 255), (obstacle_x + obstacle_width // 2, obstacle_y + obstacle_height // 2), 25)
            elif current_shape == "car":
                pygame.draw.rect(screen, (0, 255, 0), (obstacle_x, obstacle_y, obstacle_width + 30, obstacle_height - 20))  # Simulating a car
            elif current_shape == "furniture":
                pygame.draw.rect(screen, (255, 165, 0), (obstacle_x, obstacle_y, obstacle_width, obstacle_height + 50))  # Simulating furniture

           
            if mario_rect.colliderect(pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)):
                print("Collision detected!")
                collision_sound.play()  # Play collision sound
                game_over = True
                save_highest_score()  

            score_text = small_font.render(f"Score: {score}", True, (0, 0, 0))
            highest_score_text = small_font.render(f"Highest Score: {highest_score}", True, (0, 0, 0))
            screen.blit(score_text, (10, 10))
            screen.blit(highest_score_text, (10, 40))

          
            pygame.display.update()

        else:
       
            game_over_text = font.render("Game Over! Press 'R' to Retry", True, (255, 0, 0))
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))
            pygame.display.update()

        clock.tick(60)

    pygame.quit()

# ubatructions
def welcome_screen():
    screen.fill((0, 0, 0))  
    welcome_text = font.render("Welcome to Paul's Mario  Game", True, (255, 255, 255))
    instructions_text_1 = small_font.render("Instructions:", True, (255, 255, 255))
    instructions_text_2 = small_font.render("1. Press the UP arrow to jump.", True, (255, 255, 255))
    instructions_text_3 = small_font.render("2. Use LEFT and RIGHT arrows to move Mario.", True, (255, 255, 255))
    instructions_text_4 = small_font.render("3. Avoid obstacles and score points by jumping.", True, (255, 255, 255))
    instructions_text_5 = small_font.render("4. Press 'P' to pause the game.", True, (255, 255, 255))
    instructions_text_6 = small_font.render("5. Press 'R' to retry after a game over.", True, (255, 255, 255))
    start_text = small_font.render("Press any key to start...", True, (255, 255, 0))

    screen.blit(welcome_text, (SCREEN_WIDTH // 2 - welcome_text.get_width() // 2, 100))
    screen.blit(instructions_text_1, (50, 200))
    screen.blit(instructions_text_2, (50, 240))
    screen.blit(instructions_text_3, (50, 280))
    screen.blit(instructions_text_4, (50, 320))
    screen.blit(instructions_text_5, (50, 360))
    screen.blit(instructions_text_6, (50, 400))
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 500))

    pygame.display.update()

   
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def main():
    welcome_screen()  
    game_loop()  

if __name__ == "__main__":
    main()  
