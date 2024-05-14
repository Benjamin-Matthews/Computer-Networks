import socket
import pygame
import sys

# servers address and port
server = "localhost"
port = 5555

# create and connect client socket to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server, port))

# function to send a control command to the server
def send_control_input(command):
    client_socket.send(command.encode())

# fuction to receive and return game state from the server
def receive_game_state():
    game_state = client_socket.recv(1024).decode() 
    return game_state

# init pygame
pygame.init()

# size variables for the grid
grid_size = 20 # size of grid
grid_width = 20  # width of grid
grid_height = 20  # height of grid
cell_size = 35  # size of each grid cell

# calculate the size of the window 
window_width = grid_width * cell_size
window_height = grid_height * cell_size
# create the window in pygame
window = pygame.display.set_mode((window_width, window_height))


# colour definitions
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)


# function to draw the game state on the window
def display_game_state(game_state):
    # make widow black
    window.fill(black)
    # draw the grid
    for x in range(0, window_width, cell_size): # vertical lines
        pygame.draw.line(window, white, (x, 0), (x, window_height))

    for y in range(0, window_height, cell_size): # horizontal lines
        pygame.draw.line(window, white, (0, y), (window_width, y))


    # split the game state string into two parts using '|' 
    parts = game_state.split('|')

    # get the x and y positions of the snake and the food and store them in a list
    snake_pos = parts[0].split('*')
    food_pos = parts[1].split('**')
    
    # draw the food
    for pos in food_pos:
        x, y = map(int, pos[1:-1].split(',')) # get the x and y positions
        pygame.draw.rect(window, green, (x * cell_size, y * cell_size, cell_size, cell_size))

    # draw the snake
    head = False # boolean to see if head of snake has been drawn

    for pos in snake_pos:
        # if head is not drawn, draw the head of the snake
        if not head:
            x, y = map(int, pos[1:-1].split(',')) # get the x and y positions
            pygame.draw.rect(window, red, (x * cell_size, y * cell_size, cell_size, cell_size)) # draw head of snake

            # calculate the positions of the eyes
            eye1_x = x * cell_size + 10
            eye1_y = y * cell_size + 10
            eye2_x = x * cell_size + 25
            eye2_y = y * cell_size + 10

            # draw black dots as the eyes 
            pygame.draw.circle(window, black, (eye1_x, eye1_y), 5)
            pygame.draw.circle(window, black, (eye2_x, eye2_y), 5)
            
            head = True
        # else draw the body of the snake
        else:
            x, y = map(int, pos[1:-1].split(',')) # get the x and y positions
            pygame.draw.rect(window, red, (x * cell_size, y * cell_size, cell_size, cell_size))
    
    # update the window
    pygame.display.flip()


# clock variable to control the event handling frequency
clock = pygame.time.Clock()


# main game loop
while True:
    clock.tick(60)  # set frequency to 60 frames per second
    # send server get command to receive the current game state
    send_control_input("get")
    # store the current game state
    game_state = receive_game_state()
    # display current game state
    display_game_state(game_state)
    # send server control commands based on client inputs
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: # up
                send_control_input("up") 
            elif event.key == pygame.K_DOWN: # down
                send_control_input("down") 
            elif event.key == pygame.K_LEFT: # left
                send_control_input("left") 
            elif event.key == pygame.K_RIGHT: # right
                send_control_input("right") 
            elif event.key == pygame.K_r: # reset
                send_control_input("reset") 
            elif event.key == pygame.K_q: # quit
                # close pygame
                print('Closing pygame')
                pygame.quit()
                send_control_input("quit") 
                # close the client socket
                print('Closing client socket')
                client_socket.close()
                sys.exit()
            # receive current game state 
            game_state = receive_game_state() 
    



