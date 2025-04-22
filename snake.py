import os
import random
import time
import msvcrt  # For Windows keypress detection (non-blocking input)

# Node class for the linked list
class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.next = None

# Snake class using a linked list
class Snake:
    def __init__(self, x, y):
        self.head = Node(x, y)
        self.tail = self.head
        self.length = 1
    
    def move(self, x, y, grow=False):
        # Add new head
        new_head = Node(x, y)
        new_head.next = self.head
        self.head = new_head
        
        # If not growing, remove tail
        if not grow:
            current = self.head
            while current.next != self.tail:
                current = current.next
            current.next = None
            self.tail = current
        else:
            self.length += 1
    
    def get_positions(self):
        # Return all snake positions for display and collision
        positions = []
        current = self.head
        while current:
            positions.append((current.x, current.y))
            current = current.next
        return positions
    
    def check_self_collision(self):
        # Check if head collides with any body segment
        head_x, head_y = self.head.x, self.head.y
        current = self.head.next
        while current:
            if current.x == head_x and current.y == head_y:
                return True
            current = current.next
        return False

# Game settings
WIDTH = 20
HEIGHT = 20
SNAKE_CHAR = '⬜'
FOOD_CHAR = '🍎'
EMPTY_CHAR = '⬛'

# Clear console (Windows-specific, use 'clear' for Unix)
def clear_screen():
    os.system('cls')

# Display the game board
def print_board(snake, food):
    clear_screen()
    snake_positions = set(snake.get_positions())
    for y in range(HEIGHT):
        row = ''
        for x in range(WIDTH):
            if (x, y) == (snake.head.x, snake.head.y):
                row += SNAKE_CHAR  # Head of the snake
            elif (x, y) in snake_positions:
                row += '🟩'  # Body of the snake
            elif (x, y) == food:
                row += FOOD_CHAR
            else:
                row += EMPTY_CHAR
        print(row)
    

# Generate random food position not overlapping with snake
def spawn_food(snake):
    snake_positions = set(snake.get_positions())
    while True:
        food = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
        if food not in snake_positions:
            return food

# Main game loop
def game():
    # Initialize snake and food
    snake = Snake(WIDTH // 2, HEIGHT // 2)
    food = spawn_food(snake)
    direction = 'd'  # Start moving right (w=up, s=down, a=left, d=right)
    
    while True:
        # Get current head position
        head_x, head_y = snake.head.x, snake.head.y
        
        # Update direction based on input (non-blocking)
        if msvcrt.kbhit():
            key = msvcrt.getch().decode('utf-8').lower()
            if key in 'wasd' and not (
                (key == 'w' and direction == 's') or
                (key == 's' and direction == 'w') or
                (key == 'a' and direction == 'd') or
                (key == 'd' and direction == 'a')
            ):  # Prevent reversing direction
                direction = key
        
        # Calculate new head position
        if direction == 'w':
            new_x, new_y = head_x, head_y - 1
        elif direction == 's':
            new_x, new_y = head_x, head_y + 1
        elif direction == 'a':
            new_x, new_y = head_x - 1, head_y
        else:  # 'd'
            new_x, new_y = head_x + 1, head_y
        
        # Check boundaries
        if new_x < 0 or new_x >= WIDTH or new_y < 0 or new_y >= HEIGHT:
            print("boink!!! You Hit the wall.")
            break
        
        # Check if food is eaten
        grow = (new_x, new_y) == food
        snake.move(new_x, new_y, grow)
        
        # Check self-collision
        if snake.check_self_collision():
            print("Game Over! Snake ate itself.")
            break
        
        # If food eaten, spawn new food
        if grow:
            food = spawn_food(snake)
        
        # Display the game
        print_board(snake, food)
        
        # Control game speed
        time.sleep(0.1)

# Start the game
if __name__ == "__main__":
    print("Use W/A/S/D to move. Press any key to start.")
    msvcrt.getch()  # Wait for keypress to start
    game()