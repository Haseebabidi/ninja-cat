# Author: Haseeb Abidi    
# Last Edited: 3/20/2025  
# A basic test game to learn pygame  
import pygame
from sys import exit
import random



# Pygame setup
pygame.init()

# Initialize the mixer and load background music
pygame.mixer.init()
try:
    pygame.mixer.music.load('music/catmusic.wav')
    pygame.mixer.music.set_volume(0.4)  # Adjust volume (0.0 to 1.0)
    pygame.mixer.music.play(-1)         # Loop indefinitely
except pygame.error as e:
    print(f"Error loading music: {e}")

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Ninja Cat")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 20)
font2 = pygame.font.Font(None, 50)
game_active = False
start_time = 0
final_score = 0

# Level transition flags
level_2_displayed = False
level_3_displayed = False
level_4_displayed = False
level_5_displayed = False

# Function to display the score on screen
def display_score():
    current_time = (pygame.time.get_ticks() - start_time) // 1000
    score_surface = font2.render(f'Score: {current_time}', True, 'black')
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rect)
    return current_time

# Function to display a short level transition message with a custom message
def display_level_transition(message):
    transition_text = font2.render(message, True, 'white')
    transition_rect = transition_text.get_rect(center=(400, 200))
    screen.blit(transition_text, transition_rect)
    pygame.display.update()
    pygame.time.delay(2000)

# Function to display the Game Over and retry message
def try_again_screen():
    global final_score
    screen.fill('gray')
    game_over_text = font2.render('Game Over! Try Again?', True, 'white')
    game_over_rect = game_over_text.get_rect(center=(400, 180))
    final_score_text = font2.render(f'Final Score: {final_score}', True, 'white')
    final_score_rect = final_score_text.get_rect(center=(400, 230))
    retry_text = font2.render('Press SPACE to Retry', True, 'white')
    retry_rect = retry_text.get_rect(center=(400, 280))
    screen.blit(game_over_text, game_over_rect)
    screen.blit(final_score_text, final_score_rect)
    screen.blit(retry_text, retry_rect)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

# Function to show start screen with Play button
def start_screen():
    screen.fill('lightblue')
    title_text = font2.render('Ninja Cat', True, 'black')
    title_rect = title_text.get_rect(center=(400, 150))
    play_text = font2.render('Play', True, 'white')
    play_rect = pygame.Rect(350, 250, 100, 50)

    pygame.draw.rect(screen, 'purple', play_rect)
    screen.blit(title_text, title_rect)
    screen.blit(play_text, play_text.get_rect(center=play_rect.center))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    waiting = False

try:
    # Load backgrounds and objects
    background_lvl1 = pygame.image.load('graphics/city.png').convert()
    background_lvl2 = pygame.image.load('graphics/city_lvl2.png').convert()
    text = font.render("Haseeb Abidi", True, "black")

    # Load deer animation frames
    deer_frames = [
        pygame.image.load('graphics/deer1.png').convert_alpha(),
        pygame.image.load('graphics/deer2.png').convert_alpha(),
        pygame.image.load('graphics/deer3.png').convert_alpha()
    ]
    deer_index = 0
    deer_timer = 0
    deer_rect = deer_frames[0].get_rect(bottomright=(900, 360))

    # Load bat animation frames
    bat_frames = [
        pygame.image.load('graphics/bat1.png').convert_alpha(),
        pygame.image.load('graphics/bat2.png').convert_alpha(),
        pygame.image.load('graphics/bat3.png').convert_alpha(),
        pygame.image.load('graphics/bat4.png').convert_alpha()
    ]
    bat_index = 0
    bat_timer = 0
    bat_rect = bat_frames[0].get_rect(bottomright=(1200, 230))

    # Load cat animation frames
    cat_walk_frames = [
        pygame.image.load('guy/walk1.png').convert_alpha(),
        pygame.image.load('guy/walk2.png').convert_alpha(),
        pygame.image.load('guy/walk3.png').convert_alpha()
    ]
    cat_jump_frame = pygame.image.load('guy/jump.png').convert_alpha()
    cat_idle_frame = pygame.image.load('guy/idle.png').convert_alpha()

    # Initialize cat properties
    cat_walk_index = 0
    cat_walk_timer = 0
    cat_jump_timer = 0
    cat_current_image = cat_idle_frame
    cat_rect = cat_idle_frame.get_rect(midbottom=(80, 350))
    cat_gravity = 0

except pygame.error as e:
    print(f"Error loading images: {e}")
    pygame.quit()
    exit()

# Show start screen before game begins
start_screen()
game_active = True
start_time = pygame.time.get_ticks()

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                # Jump when SPACE is pressed and cat is on the ground.
                if event.key == pygame.K_SPACE and cat_rect.bottom >= 350:
                    cat_gravity = -25
                # Dash downward when S is pressed and cat is airborne.
                if event.key == pygame.K_s and cat_rect.bottom < 350:
                    cat_gravity = 25

    # Handle horizontal movement inputs
    keys = pygame.key.get_pressed()
    if game_active:
        if keys[pygame.K_d]:
            cat_rect.x += 5
            if cat_rect.right > 800:
                cat_rect.right = 800
        if keys[pygame.K_a]:
            cat_rect.x -= 5
            if cat_rect.left < 0:
                cat_rect.left = 0

    if game_active:
        current_score = (pygame.time.get_ticks() - start_time) // 1000

        # Level and speed settings based on score
        if current_score < 20:
            screen.blit(background_lvl1, (0, 0))
            speed_choices = [5, 7, 9]
        elif current_score < 50:
            if not level_2_displayed:
                display_level_transition("meow meow Level 2!")
                level_2_displayed = True
            screen.blit(background_lvl2, (0, 0))
            speed_choices = [12, 10, 9]
        elif current_score < 100:
            if not level_3_displayed:
                display_level_transition("Level 3!")
                level_3_displayed = True
            screen.blit(background_lvl2, (0, 0))
            speed_choices = [12, 18, 15]
        elif current_score < 150:
            if not level_4_displayed:
                display_level_transition("Level 4!")
                level_4_displayed = True
            screen.blit(background_lvl2, (0, 0))
            speed_choices = [18, 21, 24]
        else:
            if not level_5_displayed:
                display_level_transition("Level 5! Impossible Mode!")
                level_5_displayed = True
            screen.blit(background_lvl2, (0, 0))
            # Level 5 becomes nearly impossible with very high enemy speeds.
            speed_choices = [30, 33, 36]

        # Draw static elements
        screen.blit(text, (710, 12))

        # Move and animate deer
        deer_rect.x -= random.choice(speed_choices)
        if deer_rect.right < 0:
            deer_rect.left = random.randrange(900, 2500, 400)
        deer_timer += 1
        if deer_timer >= 6:
            deer_index = (deer_index + 1) % len(deer_frames)
            deer_timer = 0
        screen.blit(deer_frames[deer_index], deer_rect)

        # Move and animate bat (only in levels with score >= 20)
        if current_score >= 20:
            bat_rect.x -= random.choice(speed_choices)
            if bat_rect.right < 0:
                bat_rect.left = random.randrange(1500, 2200, 400)
            bat_timer += 1
            if bat_timer >= 6:
                bat_index = (bat_index + 1) % len(bat_frames)
                bat_timer = 0
            screen.blit(bat_frames[bat_index], bat_rect)

        # Apply gravity to cat
        cat_gravity += 1
        cat_rect.y += cat_gravity
        if cat_rect.bottom >= 350:
            cat_rect.bottom = 350

        # Choose animation frame for cat
        if cat_rect.bottom < 350:
            cat_jump_timer = pygame.time.get_ticks()
            cat_current_image = cat_jump_frame
            cat_rect = cat_jump_frame.get_rect(midbottom=cat_rect.midbottom)
        elif pygame.time.get_ticks() - cat_jump_timer < 100:
            cat_current_image = cat_jump_frame
            cat_rect = cat_jump_frame.get_rect(midbottom=cat_rect.midbottom)
        elif keys[pygame.K_d] or keys[pygame.K_a]:
            cat_walk_timer += 1
            if cat_walk_timer >= 6:
                cat_walk_index = (cat_walk_index + 1) % len(cat_walk_frames)
                cat_walk_timer = 0
            cat_current_image = cat_walk_frames[cat_walk_index]
            cat_rect = cat_current_image.get_rect(midbottom=cat_rect.midbottom)
        else:
            cat_current_image = cat_idle_frame
            cat_rect = cat_idle_frame.get_rect(midbottom=cat_rect.midbottom)

        screen.blit(cat_current_image, cat_rect)

        # Display score
        score_surface = font2.render(f'Score: {current_score}', True, 'black')
        score_rect = score_surface.get_rect(center=(400, 50))
        screen.blit(score_surface, score_rect)

        # Collision detection
        if deer_rect.colliderect(cat_rect) or (current_score >= 20 and bat_rect.colliderect(cat_rect)):
            game_active = False
            final_score = current_score
            try_again_screen()
            game_active = True
            # Reset objects and level flags
            deer_index = 0
            deer_rect = deer_frames[0].get_rect(bottomright=(900, 360))
            bat_index = 0
            bat_rect = bat_frames[0].get_rect(bottomright=(1200, 230))
            cat_rect.midbottom = (80, 350)
            cat_gravity = 0
            cat_walk_index = 0
            cat_walk_timer = 0
            cat_jump_timer = 0
            start_time = pygame.time.get_ticks()
            level_2_displayed = False
            level_3_displayed = False
            level_4_displayed = False
            level_5_displayed = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()
