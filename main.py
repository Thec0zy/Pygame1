import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the game window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Star Adventure")

# Load cloud image
cloud_img = pygame.image.load("Cloud1.png").convert_alpha()
cloud_img = pygame.transform.scale(cloud_img, (200, 100))  # Resize the cloud image to be larger

# Load Cola image
cola_img = pygame.image.load("Cola.png").convert_alpha()
cola_img = pygame.transform.scale(cola_img, (50, 100))  # Resize the Cola image

# Define colors
dark_blue = (0, 0, 50)
dark_purple = (38, 0, 77)
white = (255, 255, 255)
yellow = (255, 255, 0)
black = (0, 0, 0)
green = (0, 200, 0)

# Load background music
pygame.mixer.music.load("Song.mp3")

# Define glitter parameters
glitter_count = 100
glitters = [(random.randint(0, screen_width), random.randint(0, screen_height),
             random.randint(1, 3), random.randint(1, 3)) 
             for _ in range(glitter_count)]

# Main character position (center of the screen)
star_x = screen_width // 2
star_y = screen_height // 2 - 15 

# Background scrolling speed
scroll_speed = 0.05  # Even slower scrolling speed

# Star movement speed
star_speed = 1

# Cloud variables
cloud_speed = 5
clouds = []
cloud_spawn_timer = 0
cloud_spawn_delay = 50  # Adjust spawn delay for more or less frequent clouds

# Cola variables
cola_speed = 3
colas = []
cola_spawn_timer = 0
cola_spawn_delay = 500  # Adjust spawn delay for less frequent cola

# Button properties
button_color = green
button_hover_color = (0, 255, 0)
start_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 25, 200, 50)
start_button_text = pygame.font.Font(None, 24).render("START", True, white)

retry_button_rect = pygame.Rect(screen_width // 2 - 100, screen_height // 2 - 25, 100, 50)
retry_button_text = pygame.font.Font(None, 24).render("RETRY", True, white)
quit_button_rect = pygame.Rect(screen_width // 2 + 10, screen_height // 2 - 25, 100, 50)
quit_button_text = pygame.font.Font(None, 24).render("QUIT", True, white)

# Main game loop control
game_started = False
running = True
star_moving = False
move_left = False
move_right = False
move_up = False
move_down = False

# Score variables
score = 0
font = pygame.font.Font(None, 24)

# Game over flag
game_over = False

# Color transition variables
color_transition_speed = 0.001  # Speed of color transition
color_transition_t = 0  # Timer for the transition

# Flag to control text visibility
show_start_text = True

def interpolate_color(color1, color2, t):
    """Interpolate between two colors with a parameter t (0.0 to 1.0)"""
    return (
        int(color1[0] + (color2[0] - color1[0]) * t),
        int(color1[1] + (color2[1] - color1[1]) * t),
        int(color1[2] + (color2[2] - color1[2]) * t)
    )

def reset_game():
    global star_x, star_y, clouds, colas, cloud_spawn_timer, cola_spawn_timer
    global move_left, move_right, move_up, move_down, star_moving, score, game_over
    star_x = screen_width // 2
    star_y = screen_height // 2 - 15
    clouds = []
    colas = []
    cloud_spawn_timer = 0
    cola_spawn_timer = 0
    move_left = False
    move_right = False
    move_up = False
    move_down = False
    star_moving = False
    score = 0
    game_over = False
    pygame.mixer.music.play(-1)  # Restart the music when the game is reset

print("Game loop started")
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if game_started and not game_over:
                if event.key == pygame.K_a:
                    move_left = True
                elif event.key == pygame.K_d:
                    move_right = True
                elif event.key == pygame.K_w:
                    move_up = True
                elif event.key == pygame.K_s:
                    move_down = True
        elif event.type == pygame.KEYUP:
            if game_started and not game_over:
                if event.key == pygame.K_a:
                    move_left = False
                elif event.key == pygame.K_d:
                    move_right = False
                elif event.key == pygame.K_w:
                    move_up = False
                elif event.key == pygame.K_s:
                    move_down = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_button_rect.collidepoint(event.pos) and not game_started:
                game_started = True
                show_start_text = False  # Hide the start text when the game starts
                reset_game()                 
            if retry_button_rect.collidepoint(event.pos) and game_over:
                reset_game()
                game_started = True
            if quit_button_rect.collidepoint(event.pos) and game_over:
                running = False

    # Fill the screen with dark blue
    if color_transition_t < 0.5:
        current_color = interpolate_color(dark_blue, dark_purple, color_transition_t * 2)
    else:
        current_color = interpolate_color(dark_purple, dark_blue, (color_transition_t - 0.5) * 2)
    screen.fill(current_color)

    color_transition_t = (color_transition_t + color_transition_speed) % 1.0

    if game_started and not game_over:
        # Move the star left or right based on key states
        if move_left:
            star_x -= star_speed  # Move left
            if star_x < 50:  # Left boundary position
                star_x = 50  # Adjust the star position back to the boundary
        if move_right:
            star_x += star_speed  # Move right
            if star_x > screen_width - 50:  # Right boundary position
                star_x = screen_width - 50  # Adjust the star position back to the boundary
        
        # Move the star up or down based on key states
        if move_up:
            star_y -= star_speed  # Move up
            if star_y < 50:  # Top boundary position
                star_y = 50  # Adjust the star position back to the boundary
        if move_down:
            star_y += star_speed  # Move down
            if star_y > screen_height - 50:  # Bottom boundary position
                star_y = screen_height - 50  # Adjust the star position back to the boundary

        # Spawn new clouds
        cloud_spawn_timer += 1
        if cloud_spawn_timer >= cloud_spawn_delay:
            if len(clouds) < 3:  # Limit the number of clouds
                cloud_x = random.randint(0, screen_width - cloud_img.get_width())
                cloud_y = random.randint(-200, -50)  # Place above the screen
                clouds.append((cloud_x, cloud_y))
            cloud_spawn_timer = 0

        # Move the clouds
        for i in range(len(clouds)):
            cloud_x, cloud_y = clouds[i]
            cloud_y += scroll_speed * cloud_speed  # Move cloud down
            clouds[i] = (cloud_x, cloud_y)
            
            # Remove clouds that have fallen off the screen
            if cloud_y > screen_height:
                clouds.pop(i)
                break

        # Spawn new cola
        cola_spawn_timer += 1
        if cola_spawn_timer >= cola_spawn_delay:
            if len(colas) < 1:  # Limit the number of cola
                cola_x = random.randint(0, screen_width - cola_img.get_width())
                cola_y = random.randint(-200, -50)  # Place above the screen
                colas.append((cola_x, cola_y))
            cola_spawn_timer = 0

        # Move the cola
        for i in range(len(colas)):
            cola_x, cola_y = colas[i]
            cola_y += scroll_speed * cola_speed  # Move cola down
            colas[i] = (cola_x, cola_y)
            
            # Remove cola that have fallen off the screen
            if cola_y > screen_height:
                colas.pop(i)
                break

        # Move the glitters along with the background
        for i in range(len(glitters)):
            glitter_x, glitter_y, _, glitter_speed = glitters[i]
            glitters[i] = (glitter_x, (glitter_y + scroll_speed * glitter_speed) % screen_height,
                           glitters[i][2], glitters[i][3])

        # Draw clouds
        for cloud in clouds:
            screen.blit(cloud_img, cloud)

        # Draw cola
        for cola in colas:
            screen.blit(cola_img, cola)

        # Draw glitter effects
        for glitter in glitters:
            pygame.draw.circle(screen, white, (glitter[0], glitter[1]), random.randint(1, 3))

        # Draw the star
        star_points = [(star_x, star_y - 30), (star_x + 10, star_y - 10), (star_x + 40, star_y - 10),
                       (star_x + 20, star_y + 10), (star_x + 30, star_y + 40),
                       (star_x, star_y + 20), (star_x - 30, star_y + 40),
                       (star_x - 20, star_y + 10), (star_x - 40, star_y - 10),
                       (star_x - 10, star_y - 10)]
        pygame.draw.polygon(screen, yellow, star_points, 5)

        # Check for collision with clouds
        star_rect = pygame.Rect(star_x - 20, star_y - 30, 40, 70)
        for cloud_x, cloud_y in clouds:
            cloud_rect = pygame.Rect(cloud_x, cloud_y, cloud_img.get_width(), cloud_img.get_height())
            if star_rect.colliderect(cloud_rect):
                game_over = True
                pygame.mixer.music.stop()  # Stop the music when the star hits a cloud

        # Check for collision with colas
        for cola_x, cola_y in colas:
            cola_rect = pygame.Rect(cola_x, cola_y, cola_img.get_width(), cola_img.get_height())
            if star_rect.colliderect(cola_rect):
                colas.remove((cola_x, cola_y))
                score += 1

        # Display score
        score_text = font.render(f"Score: {score}", True, white)
        screen.blit(score_text, (10, 10))

    # If game over, display game over text, score, retry button, and quit button
    if game_over:
        screen.fill(black)
        game_over_text = font.render("Oww man!", True, white)
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, 150))
        score_text = font.render(f"Total Score: {score}", True, white)
        screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 200))

        # Draw retry button
        mouse_pos = pygame.mouse.get_pos()
        retry_color_to_use = button_hover_color if retry_button_rect.collidepoint(mouse_pos) else green  # Change button color back to green
        pygame.draw.rect(screen, retry_color_to_use, retry_button_rect)
        screen.blit(retry_button_text, (retry_button_rect.x + (retry_button_rect.width - retry_button_text.get_width()) // 2,
                                        retry_button_rect.y + (retry_button_rect.height - retry_button_text.get_height()) // 2))

        # Draw quit button
        quit_color_to_use = button_hover_color if quit_button_rect.collidepoint(mouse_pos) else green  # Change button color back to green
        pygame.draw.rect(screen, quit_color_to_use, quit_button_rect)
        screen.blit(quit_button_text, (quit_button_rect.x + (quit_button_rect.width - quit_button_text.get_width()) // 2,
                                       quit_button_rect.y + (quit_button_rect.height - quit_button_text.get_height()) // 2))

    elif not game_started:
        # Draw start button
        mouse_pos = pygame.mouse.get_pos()
        start_color_to_use = button_hover_color if start_button_rect.collidepoint(mouse_pos) else green  # Change button color back to green
        pygame.draw.rect(screen, start_color_to_use, start_button_rect)
        screen.blit(start_button_text, (start_button_rect.x + (start_button_rect.width -
start_button_text.get_width()) // 2,
                                        start_button_rect.y + (start_button_rect.height - start_button_text.get_height()) // 2))

        # Add text above the start button
    if show_start_text:
        welcome_text = font.render("Welcome! You're about to meet Patrick, a diabetic, coke addict, flying without a spaceship.", True, white)
        screen.blit(welcome_text, (screen_width // 2 - welcome_text.get_width() // 2, start_button_rect.y - 80))  # Adjust vertical position

        # Add ASWD keys in little squares
        aswd_text = font.render("To move around, use", True, white)
        screen.blit(aswd_text, (screen_width // 2 - aswd_text.get_width() - 10, start_button_rect.y - 130))  # Adjust vertical position

        # Draw little squares for ASWD keys
        pygame.draw.rect(screen, black, (screen_width // 2 + 10, start_button_rect.y - 125, 30, 30))
        pygame.draw.rect(screen, black, (screen_width // 2 + 50, start_button_rect.y - 125, 30, 30))
        pygame.draw.rect(screen, black, (screen_width // 2 + 90, start_button_rect.y - 125, 30, 30))
        pygame.draw.rect(screen, black, (screen_width // 2 + 130, start_button_rect.y - 125, 30, 30))

        # Draw ASWD keys
        a_key = font.render("A", True, white)
        s_key = font.render("S", True, white)
        w_key = font.render("W", True, white)
        d_key = font.render("D", True, white)
        screen.blit(a_key, (screen_width // 2 + 20, start_button_rect.y - 115))
        screen.blit(s_key, (screen_width // 2 + 60, start_button_rect.y - 115))
        screen.blit(w_key, (screen_width // 2 + 100, start_button_rect.y - 115))
        screen.blit(d_key, (screen_width // 2 + 140, start_button_rect.y - 115))

    # Update the display
    pygame.display.flip()

print("Game loop ended")

# Quit Pygame
pygame.quit()
sys.exit()

