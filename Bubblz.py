import pygame
import random
import math

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 600
wn = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bubblz")
run = True
clock = pygame.time.Clock()
fps = 60
game_state = "menu" 
spawn_interval = 2000  
last_spawn_time = pygame.time.get_ticks()
lives = 3
bubbles_available = 30

background_image = pygame.image.load('assets/sea.jpg')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

logo_image = pygame.image.load('assets/logo.png')
logo_rect = logo_image.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 50))
logo_angle = 0

logo2_image = pygame.image.load('assets/logo2.png')

# Dot properties
dot_color = (255, 0, 0)  
dot_radius = 10  
dot_position = (0, 0)  

star_frames = []  # List to store star frames
for i in range(15):
    frame = pygame.image.load(f'assets/star/output-onlinegiftools_{i}.png').convert_alpha()
    star_frames.append(frame)

STAR_SIZE = (50, 50)  # Adjust the size of the star
star_frames_rescaled = [pygame.transform.scale(frame, STAR_SIZE) for frame in star_frames]  # Rescale star frames

frame_rate = 5  # Adjust the frame rate (lower value for slower movement)
frame_counter = 0  # Counter to control frame rate

current_frame = 0  # Variable to track the current frame of the star gif
dot_position = (0, 0)  # Initial position for the star


# Load spikeball image
spikeball_img = pygame.image.load('assets/spikeball.png')
spikeball_img = pygame.transform.scale(spikeball_img, (50, 50))

# Spikeball properties
spikeball_pos = [0, 0]  # Initial position
spikeball_speed = 2  # Movement speed
directions = [-1, 1]  # Movement direction options
wave_amplitude = 100  # Amplitude of the sine wave
wave_frequency = 0.01  # Frequency of the sine wave

# Colors
WHITE = (255, 255, 255)





pygame.mixer.set_num_channels(16)  

pygame.mixer.music.load('assets/CatOnWindow105.mp3') 
pygame.mixer.music.play(-1) 

def create_star():
    global dot_position
    # Generate random position for the star
    x = random.randint(STAR_SIZE[0] // 2, WIDTH - STAR_SIZE[0] // 2)
    y = random.randint(STAR_SIZE[1] // 2, HEIGHT - STAR_SIZE[1] // 2)
    dot_position = (x, y)


def draw_star():
    global current_frame, frame_counter
    # Draw the current frame of the star gif
    wn.blit(star_frames_rescaled[current_frame], (dot_position[0] - STAR_SIZE[0] // 2, dot_position[1] - STAR_SIZE[1] // 2))
    # Update current frame for next iteration based on frame rate
    frame_counter += 1
    if frame_counter >= frame_rate:
        current_frame = (current_frame + 1) % len(star_frames)
        frame_counter = 0

custom_font_path = 'assets/Krabby Patty.ttf'
custom_font = pygame.font.Font(custom_font_path, 28)  


bubbleImg = pygame.transform.scale(pygame.image.load('assets/bubble.png'), (70, 70))
numofBubbles = 35
bubbles = []

spikeCursor = pygame.transform.scale(pygame.image.load('assets/spikeball.png'), (30, 30))

def show_game_stats():
    # Render text for number of bubbles
    bubbles_text = custom_font.render(f"Bubbles: {len(bubbles)}", True, (0, 0, 0))
    wn.blit(bubbles_text, (10, 10))
    
    # Display lives using spikeball images
    life_icon_size = 30  # Size of the life icon
    life_icon_img = pygame.transform.scale(spikeCursor, (life_icon_size, life_icon_size))
    for i in range(lives):
        wn.blit(life_icon_img, (10 + i * (life_icon_size + 5), 40))  # Adjust positioning as needed


def create_dot():
    global dot_position
    while True:
        x = random.randint(dot_radius, WIDTH - dot_radius)
        y = random.randint(dot_radius, HEIGHT - dot_radius)
       
        if not (WIDTH / 3 < x < 2 * WIDTH / 3 and HEIGHT / 3 < y < 2 * HEIGHT / 3):
            dot_position = (x, y)
            break

def check_dot_collision(spike_pos):
    global game_state, dot_position
    spike_center_x = spike_pos[0] + spikeCursor.get_width() // 2
    spike_center_y = spike_pos[1] + spikeCursor.get_height() // 2
    dot_x, dot_y = dot_position
    distance_squared = (spike_center_x - dot_x) ** 2 + (spike_center_y - dot_y) ** 2
    collision_threshold = (dot_radius + 10) ** 2  

    if distance_squared <= collision_threshold:
        
        for _ in range(7):
            if bubbles:
                bubbles.pop()
      
        create_dot()  
        game_state = "game"  

question_button_image = pygame.image.load('assets/question.png')
question_button_image = pygame.transform.scale(question_button_image, (50, 50))
question_button_rect = question_button_image.get_rect(topright=(WIDTH - 10, 10))






def draw_dot():
    pygame.draw.circle(wn, dot_color, dot_position, dot_radius)


def create_bubbles():
    bubbles.clear()
    for i in range(numofBubbles):
       
        while True:
            bubbleX = random.randint(0, WIDTH - 70)
            bubbleY = random.randint(0, HEIGHT - 70)
            if not (WIDTH / 3 < bubbleX < 2 * WIDTH / 3 and HEIGHT / 3 < bubbleY < 2 * HEIGHT / 3):
                break
        bubbleVelX, bubbleVelY = random.choice([-2, 2]), random.choice([-2, 2])
        bubbles.append({"position": [bubbleX, bubbleY], "velocity": [bubbleVelX, bubbleVelY]})

def move_bubbles():
    global lives, game_state
    for bubble in list(bubbles):
        bubbleX, bubbleY = bubble["position"]
        bubbleVelX, bubbleVelY = bubble["velocity"]
        bubbleX += bubbleVelX
        bubbleY += bubbleVelY
        
        # Handle bubble wall collisions
        if bubbleX >= WIDTH - 70 or bubbleX <= 0:
            bubble["velocity"][0] *= -1
        if bubbleY <= 0 or bubbleY >= HEIGHT - 70:
            bubble["velocity"][1] *= -1
        bubble["position"] = [bubbleX, bubbleY]

        # Check collision with spike cursor
        spike_pos = pygame.mouse.get_pos()
        spike_center_x = spike_pos[0] + spikeCursor.get_width() / 2
        spike_center_y = spike_pos[1] + spikeCursor.get_height() / 2
        if (spike_center_x - (bubbleX + 35))**2 + (spike_center_y - (bubbleY + 35))**2 <= (35)**2:
            lives -= 1  # Decrease life
            bubbles.remove(bubble)
            if lives == 0:
                game_state = "end"
            break

def create_bubble(avoid_area):
    while True:
        bubbleX = random.randint(0, WIDTH - 70)
        bubbleY = random.randint(0, HEIGHT - 70)
        if not (avoid_area.collidepoint(bubbleX, bubbleY) or avoid_area.collidepoint(bubbleX + 70, bubbleY + 70)):
            break
    bubbleVelX, bubbleVelY = random.choice([-2, 2]), random.choice([-2, 2])
    bubbles.append({"position": [bubbleX, bubbleY], "velocity": [bubbleVelX, bubbleVelY]})


def draw_bubbles():
    for bubble in bubbles:
        wn.blit(bubbleImg, bubble["position"])

'''
def pop_bubble_with_spike(spike_pos):
    for i, bubble in sorted(enumerate(bubbles), reverse=True):
        bubbleX, bubbleY = bubble["position"]
        bubble_center_x = bubbleX + bubbleImg.get_width() / 2
        bubble_center_y = bubbleY + bubbleImg.get_height() / 2
        spike_center_x = spike_pos[0] + spikeCursor.get_width() / 2
        spike_center_y = spike_pos[1] + spikeCursor.get_height() / 2
        if (spike_center_x - bubble_center_x) ** 2 + (spike_center_y - bubble_center_y) ** 2 <= (bubbleImg.get_width() / 2) ** 2:
            sound = pygame.mixer.Sound('assets/bubble.mp3')
            sound.play()
            del bubbles[i]
            break
'''

def check_spike_collision(player_spike_pos, floating_spike_pos):
    global lives
    player_spike_center_x = player_spike_pos[0] + spikeCursor.get_width() // 2
    player_spike_center_y = player_spike_pos[1] + spikeCursor.get_height() // 2
    floating_spike_center_x = floating_spike_pos[0] + spikeball_img.get_width() // 2
    floating_spike_center_y = floating_spike_pos[1] + spikeball_img.get_height() // 2

    distance_squared = (player_spike_center_x - floating_spike_center_x) ** 2 + (player_spike_center_y - floating_spike_center_y) ** 2
    collision_threshold = ((spikeCursor.get_width() // 2) + (spikeball_img.get_width() // 2)) ** 2

    if distance_squared <= collision_threshold:
        if lives < 3:  # Ensure lives do not exceed 3
            lives += 1
        return True
    return False


def pop_bubble_with_spike(spike_pos):
    for i, bubble in sorted(enumerate(bubbles), reverse=True):
        bubble_rect = bubbleImg.get_rect(topleft=bubble["position"])
        bubble_center_x = bubble_rect.centerx
        bubble_center_y = bubble_rect.centery
        spike_tip_rect = pygame.Rect(spike_pos[0] + 10, spike_pos[1] + 10, 10, 10)
        if (spike_tip_rect.centerx - bubble_center_x) ** 2 + (spike_tip_rect.centery - bubble_center_y) ** 2 <= 10 ** 2:
            sound = pygame.mixer.Sound('assets/bubble.mp3')
            sound.play()
            del bubbles[i]
            break


def show_menu():
    global logo_angle, logo2_surface
    wn.blit(background_image, (0, 0))

    # Update logo_angle using the sine function for the waving effect of logo1
    logo_angle += 0.05
    logo_rect.centery = HEIGHT / 2 + math.sin(logo_angle) * 50
    wn.blit(logo_image, logo_rect)

    # Handle logo2 with pulsating effect
    if 'logo2_surface' not in globals():
        logo2_surface = pygame.Surface((logo2_image.get_width(), logo2_image.get_height()), pygame.SRCALPHA)
        logo2_surface.blit(logo2_image, (0, 0))
    opacity = int(128 + 127 * math.sin(pygame.time.get_ticks() / 300))
    logo2_surface.set_alpha(opacity)
    logo2_x, logo2_y = 170, 450
    wn.blit(logo2_surface, (logo2_x, logo2_y))
    wn.blit(question_button_image, question_button_rect)

def show_end_screen():
    wn.blit(background_image, (0,0))
    end_font = pygame.font.SysFont(None, 55)
    end_text = custom_font.render("Game Over, Click to Restart", True, (0, 0, 0))
    text_rect = end_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    wn.blit(end_text, text_rect)

def reset_game():
    global lives, last_spawn_time, game_state, bubbles
    lives = 3  
    last_spawn_time = pygame.time.get_ticks() 
    bubbles.clear()  
    game_state = "menu"  

while run:
    current_time = pygame.time.get_ticks()
    if game_state == "game" and current_time - last_spawn_time >= spawn_interval:
        last_spawn_time = current_time
        mouse_pos = pygame.mouse.get_pos()
        avoid_area = pygame.Rect(mouse_pos[0] - 100, mouse_pos[1] - 100, 200, 200)
        create_bubble(avoid_area)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state in ["end", "win"]:
                reset_game()
        elif event.type == pygame.KEYDOWN:
            if game_state == "menu":
                game_state = "game"
                create_bubbles()
                pygame.mouse.set_pos(WIDTH / 2, HEIGHT / 2)
                pygame.mouse.set_visible(False)

    if game_state == "menu":
        create_star()
        draw_star()
        show_menu()
        pygame.mouse.set_visible(True)
    elif game_state == "game":
        wn.blit(background_image, (0,0))
        show_game_stats()
        move_bubbles()
        draw_bubbles()
        draw_star()
        spikeball_pos[0] += directions[0] * spikeball_speed
        spikeball_pos[1] += directions[1] * spikeball_speed * math.sin(wave_frequency * spikeball_pos[0])
        spikeball_pos[0] %= WIDTH
        spikeball_pos[1] %= HEIGHT
        wn.blit(spikeball_img, (spikeball_pos[0], spikeball_pos[1]))
        spike_pos = pygame.mouse.get_pos()
        cursor_pos = (spike_pos[0] - spikeCursor.get_width() // 2, spike_pos[1] - spikeCursor.get_height() // 2)
        pop_bubble_with_spike(cursor_pos)
        check_dot_collision(spike_pos)


        if check_spike_collision(spike_pos, spikeball_pos):
            spikeball_pos = [random.randint(0, WIDTH - 50), random.randint(0, HEIGHT - 50)]  # Reset floating spike position
        wn.blit(spikeCursor, cursor_pos)


        
    elif game_state == "end":
        show_end_screen()
        pygame.mouse.set_visible(True)
    elif game_state == "win":
        wn.fill(WHITE)
        win_text = custom_font.render("Congratulations, Click to Restart", True, (0, 0, 0))
        text_rect = win_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        wn.blit(win_text, text_rect)

    pygame.display.update()
    clock.tick(fps)