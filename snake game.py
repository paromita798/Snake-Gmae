import tkinter
import random
import pygame

# Game constants
ROWS = 25
COLS = 25
TILE_SIZE = 25
WINDOW_WIDTH = TILE_SIZE * COLS
WINDOW_HEIGHT = TILE_SIZE * ROWS

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Initialize pygame mixer
pygame.mixer.init()
eat_sound = pygame.mixer.Sound("Snake Hiss 1 - QuickSounds.com.mp3")
game_over_sound = pygame.mixer.Sound("fail-234710.mp3")
pygame.mixer.music.load("game-background-359782.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)  # Loop forever

# Game window setup
window = tkinter.Tk()
window.title("Snake with Sound")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg="white", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=0, highlightthickness=0)
canvas.pack()
window.update()

# Center the window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry(f"{window_width}x{window_height}+{(screen_width - window_width) // 2}+{(screen_height - window_height) // 2}")

# Initialize game state
snake = Tile(TILE_SIZE * 5, TILE_SIZE * 5)
food = Tile(TILE_SIZE * 10, TILE_SIZE * 10)
velocityX, velocityY = 0, 0
snake_body = []
game_over = False
score = 0

def change_direction(e):
    global velocityX, velocityY, game_over
    if game_over:
        return
    if e.keysym == "Up" and velocityY != 1:
        velocityX, velocityY = 0, -1
    elif e.keysym == "Down" and velocityY != -1:
        velocityX, velocityY = 0, 1
    elif e.keysym == "Left" and velocityX != 1:
        velocityX, velocityY = -1, 0
    elif e.keysym == "Right" and velocityX != -1:
        velocityX, velocityY = 1, 0

def move():
    global snake, food, snake_body, game_over, score

    if game_over:
        return

    # Check wall collision
    if snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT:
        pygame.mixer.Sound.play(game_over_sound)
        game_over = True
        return

    # Check self collision
    for tile in snake_body:
        if snake.x == tile.x and snake.y == tile.y:
            pygame.mixer.Sound.play(game_over_sound)
            game_over = True
            return

    # Check food collision
    if snake.x == food.x and snake.y == food.y:
        pygame.mixer.Sound.play(eat_sound)
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0, COLS - 1) * TILE_SIZE
        food.y = random.randint(0, ROWS - 1) * TILE_SIZE
        score += 1

    # Move snake body
    for i in range(len(snake_body) - 1, -1, -1):
        if i == 0:
            snake_body[i].x = snake.x
            snake_body[i].y = snake.y
        else:
            snake_body[i].x = snake_body[i - 1].x
            snake_body[i].y = snake_body[i - 1].y

    # Move head
    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE

def draw():
    global snake, food, snake_body, game_over, score

    move()
    canvas.delete("all")

    # Draw food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill='red')

    # Draw head
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill='lime green', outline='black')

    # Draw body
    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill='lime green', outline='black')

    # Display score / game over
    if game_over:
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font="Arial 20", text=f"Game Over: {score}", fill="white")
    else:
        canvas.create_text(30, 20, font="Arial 10", text=f"Score: {score}", fill="white")

    window.after(100, draw)

# Bind keys and start game
window.bind("<KeyRelease>", change_direction)
draw()
window.mainloop()
