import pygame
import time
import random
import sys
pygame.font.init()

WIDTH, HEIGHT = 800, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

BG = pygame.transform.scale(pygame.image.load("bg.jpeg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60

PLAYER_VEL = 5
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 3
PARTICLE_COUNT = 30
PARTICLE_DURATION = 1000  # Duration in milliseconds for displaying particles
PARTICLE_SIZE = 5
PARTICLE_VEL = 2
PARTICLE_RADIUS = 20
FONT = pygame.font.SysFont("comicsans", 30)


def draw(player, elapsed_time, stars, score, high_score):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    score_text = FONT.render(f"Score: {score}", 1, "white")
    WIN.blit(score_text, (10, 50))

    high_score_text = FONT.render(f"High Score: {high_score}", 1, "white")
    WIN.blit(high_score_text, (10, 90))

    pygame.draw.rect(WIN, "red", player)

    for star in stars:
        pygame.draw.rect(WIN, "white", star)
    particles = []
    for particle in particles:
        color, particle_x, particle_y = particle
        pygame.draw.circle(WIN, color, (particle_x, particle_y), PARTICLE_RADIUS)

    pygame.display.update()

def play_again_prompt():
    prompt_rect = pygame.Rect(200, 220, 450, 100)
    yes_button_rect = pygame.Rect(250, 300, 100, 50)
    no_button_rect = pygame.Rect(450, 300, 100, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if yes_button_rect.collidepoint(mouse_pos):
                    return True
                elif no_button_rect.collidepoint(mouse_pos):
                    return False

        pygame.draw.rect(WIN, "indigo", prompt_rect)
        pygame.draw.rect(WIN, "green", yes_button_rect)
        pygame.draw.rect(WIN, "red", no_button_rect)

        prompt_text = FONT.render("Do you want to play again?", 1, "white")
        yes_button_text = FONT.render("Yes", 1, "white")
        no_button_text = FONT.render("No", 1, "white")
        load_high_score()
        WIN.blit(prompt_text,(250, 250))
        WIN.blit(yes_button_text, (275, 310))
        WIN.blit(no_button_text, (475, 315))

        pygame.display.update()

def game_over(score, high_score):
    if score > high_score:
        high_score = score
        save_high_score(high_score)  # Save the new high score to a file
    lost_text = FONT.render("You Lost!", 1, "white")
    WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(1000)
    return play_again_prompt()

def main():
    run = True
def main():
    run = True                                 #variable to control the game loop.

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)  #Rectangular object representing a player
    clock = pygame.time.Clock()  #creates a clock object using the pygame.time.Clock() constructor.
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000     #time interval where the stars are added.
    star_count = 0                #track of time till last star was added.

    stars = []
    hit = False

    score = 0
    high_score = load_high_score()
    while run:
        #The clock.tick() function helps maintain a consistent frame rate for the game.
        # This ensures that the game runs smoothly and consistently on different systems.
        star_count += clock.tick(60) #the game to run at approximately 60 frames per second.
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break
            else:
                score += 1  # Increment the score when a star is successfully dodged

        if hit:
            if score > high_score:
                high_score = score
                save_high_score(high_score)  # Save the new high score to a file
            lost_text = FONT.render("You Lost!", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(1000)
            play_again = play_again_prompt()
            if play_again:
                player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
                star_add_increment = 2000
                star_count = 0
                stars = []
                hit = False
                score = 0
                continue
            else:
                print(high_score)
                break
        draw(player, elapsed_time, stars, score, high_score)

    pygame.quit()


def load_high_score():
    # Load the high score from a file or return 0 if the file doesn't exist
    try:
        with open("high_score.txt", "r") as file:
            high_score = int(file.read())
            return high_score
    except FileNotFoundError:
        return 0

def save_high_score(high_score):
    # Save the high score to a file
    with open("high_score.txt", "w") as file:
        file.write(str(high_score))


if __name__ == "__main__":
    main()
