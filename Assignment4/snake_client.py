import numpy as np
import pygame
import time
import socket
import pickle

width = 500
height = 500
rows = 20

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server = "localhost"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
        except:
            print(f"Unable to connect to server")

    def send(self, data, receive=False):
        try:
            self.client.send(str.encode(data))
            if receive:
                # decode and split result
                result = self.client.recv(2048).decode()
                return tuple(result.split("|"))
            else:
                return None
        except socket.error as e:
            print(e)

    def recv(self):
        try:
            return self.client.recv(2048).decode()
        except socket.timeout as e:
            return None

# colour definitions
rgb_colors = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "orange": (255, 165, 0),
}
rgb_colors_list = list(rgb_colors.values())

# draw grid
def drawGrid(w, surface):
    global rows
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))

# drawing functions
def drawThings(surface, positions, color=None, eye=False):
    global width, rgb_colors_list
    dis = width // rows
    if color is None:
        color = (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))
    for pos_id, pos in enumerate(positions):
        i, j = pos

        pygame.draw.rect(surface, color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eye and pos_id == 0:
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)

def draw(surface, players, snacks):
    global rgb_colors_list

    surface.fill((0, 0, 0))
    drawGrid(width, surface)

    player_colors = {}  # dictionary to store player colours based on pos

    for player in players:
        pos_str = str(player)  # convert player pos to str
        if pos_str not in player_colors:
            # assign a new colour if player not in dict 
            player_colors[pos_str] = rgb_colors_list[len(player_colors) % len(rgb_colors_list)]

        color = player_colors[pos_str]
        drawThings(surface, player, color=color, eye=True)

    drawThings(surface, snacks, (0, 255, 0))
    pygame.display.update()





def main():
    pygame.init()  # pygame init

    win = pygame.display.set_mode((width, height))
    n = Network()
    flag = True

    clock = pygame.time.Clock()  # clock for fps


    while flag:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                flag = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    n.send("left")
                elif event.key == pygame.K_RIGHT:
                    n.send("right")
                elif event.key == pygame.K_UP:
                    n.send("up")
                elif event.key == pygame.K_DOWN:
                    n.send("down")


        result = n.send("get", receive=True)
        if result:
            try:
                *positions, messages = result
            except ValueError:
                continue

            snacks, players = [], []

            for pos in positions:
                raw_players = pos.split("**")
                raw_snacks = messages.split("**")

                # Parse players and snacks from the received game state
                if raw_players == '':
                    pass
                else:
                    for raw_player in raw_players:
                        raw_positions = raw_player.split("*")
                        if len(raw_positions) == 0:
                            continue

                        positions = []
                        for raw_position in raw_positions:
                            if raw_position == "":
                                continue
                            nums = raw_position.split(')')[0].split('(')[1].split(',')
                            positions.append((int(nums[0]), int(nums[1])))
                        players.append(positions)

                if len(raw_snacks) == 0:
                    continue

                for i in range(len(raw_snacks)):
                    nums = raw_snacks[i].split(')')[0].split('(')[1].split(',')
                    snacks.append((int(nums[0]), int(nums[1])))
            draw(win, players, snacks)

        clock.tick(10)  # fps of game

    pygame.quit() 
if __name__ == "__main__":
    main()