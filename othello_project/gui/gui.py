import os
import sys
import threading
import requests
import socketio

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(project_dir)

from typing import List, Tuple
from math import sqrt
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pygame.locals import *
import click 
from othello_project.gui.reversi import Reversi, ReversiPiece
from typing import Optional


# Set up your HTML canvas size (adjust as needed)
canvas_width, canvas_height = 600, 600


sio = socketio.Client()

def send_message_to_server(message):
    sio.emit('message_from_client', message)

def handle_server_message(message):
    # Handle messages received from the server (e.g., updates from other clients)
    pass

sio.connect('http://127.0.0.1:5000')

@sio.on('message_from_server')
def handle_message_from_server(message):
    # Handle messages received from the server
    handle_server_message(message)

class GUI_it:
    """
    Class for a GUI-based bitmap editor
    """

    window : int
    border : int
    grid : List[List[bool]]
    surface : pygame.surface.Surface
    clock : pygame.time.Clock
    
    def __init__(self, game: Reversi, window: int = 600, border: int = 40,
                 cells_side: int = 32):
        """
        Constructor
        Parameters:
            window : int : height of window
            border : int : number of pixels to use as border around elements
            cells_side : int : number of cells on a side of a square bitmap grid
        """

        self.window: int = window
        self.border: int = border
        self.in_grid: bool = False
        #self.game: Reversi = Reversi(board_size, 2, True)

        # Initialize Pygame
        pygame.init()
        # Set window title
        pygame.display.set_caption("Reversi")
        # Set window size
        self.surface = pygame.display.set_mode((window + border + cells_side,
                                                window))
        self.clock = pygame.time.Clock()

        self.game: Reversi = game

        # #Music
        # pygame.mixer.music.load("othello_project/gui/media/bg_music.mp3", "mp3")
        # pygame.mixer.music.play(-1, start = 0.0, fade_ms=0)

        self.initialize_game_state()

        self.event_loop(game)
    
    def initialize_game_state(self):
    # Make an HTTP GET request to the Flask API endpoint to get the game state
    # Parse the JSON response and set the game state in your GUI
    # Example:
        response = requests.get('https://othello-sk.herokuapp.com/api/get_game_state')
        if response.status_code == 200:
            game_state = response.json()
            # Set the game state in your GUI
        else: 
            return 'ERROR'
            

    @property
    def cells_side(self):
        """Number of rows/ columns grid is split into"""
        return self.game.size

    @property
    def square(self) -> int:
        """Length of side of each square in cell"""
        return (self.window - 2 * self.border) // self.cells_side

    @property
    def x_bounds(self) -> Tuple[int, int]:
        """
        Bounds of grid: x
        Inputs: None except self
        Returns (Tuple[int, int]): x min, x max within grid
        """
        return (0 + self.border, self.window - self.border)

    @property
    def y_bounds(self) -> Tuple[int, int]:
        """
        Bounds of grid: y
        Inputs: None except self
        Returns (Tuple[int, int]): y min, y max within grid
        """
        return(0 + self.border, self.window - self.border)
    
    def cell_loc(self, x, y) -> Tuple[int, int]:
        """
        Converts location of cursor within grid to row and col it's in
        Inputs: 
            x (int): x location of cursor
            y (int): y location of cursor
        Returns (Tuple[int, int]): column and row of cell cursor is in
        """
        grid_col: int = min(int((x - self.x_bounds[0])// self.square), self.game.size)
        grid_row: int = min(int((y - self.y_bounds[0])// self.square), self.game.size)
        return(grid_row, grid_col)

    def where_mouse(self, pos: Tuple[int, int]) -> None:
        """
        Checks whether mouse is in the grid. 

        Inputs:
            pos(Tuple[int, int]): Position of mourse cursor

        Returns: nothing
        """
        x, y = pos
        if x >= self.x_bounds[0] and x < self.x_bounds[1] and\
            y >= self.y_bounds[0] and y < self.y_bounds[1]:
            self.in_grid = True


    def draw_window(self, game: Reversi) -> None:
        """
        Draws the contents of the window
        Parameters: none beyond self
        Returns: nothing
        """
        n = game.num_players
        board_col = (180, 178, 170)
        pos_color = (0, 100, 0)
        black = (0, 0, 0)
        white = (255, 255, 255)

        colors = [ (255, 255, 224), 
                  (238, 130, 238), 
                  (173, 255, 47), 
                  (102, 205, 170), 
                  (0, 0, 205), 
                  (211, 211, 211), 
                  (85, 107, 47),
                  (165, 42, 42),
                  (0, 0, 0)]

        player_colors: List[Tuple[int, int, int]] = colors[:n]
        
        # Background
        if game.done:
            self.surface.fill(pos_color)
            font_size: int = round(self.window / 24)
            text_display: str = str("Game is done! Player(s) " + str(game.outcome) + " won!")
            font = pygame.font.SysFont('Arial', font_size)
            text = font.render(text_display, True, white)
            self.surface.blit(text, ((self.x_bounds[0], (self.y_bounds[0] + self.y_bounds[1])/2)))

        else:
            self.surface.fill((128, 128, 128))
            for row in range(self.cells_side):
                for col in range(self.cells_side):
                    rect = (self.border + col * self.square,
                            self.border + row * self.square,
                            self.square, self.square)
                    fill = board_col
                    pygame.draw.rect(self.surface, color=fill,
                                    rect=rect)
                    pygame.draw.rect(self.surface, color=black,
                                        rect=rect, width=1)
                    cell: Optional[int] = self.game.grid[row][col]
                    if isinstance(cell, int) and cell in range(n + 1):
                        fill = player_colors[cell - 1]
                        pygame.draw.rect(self.surface, color=fill,
                                    rect=rect)
            
            for row, col in game.available_moves:
                fill = pos_color
                rect = (self.border + col * self.square,
                            self.border + row * self.square,
                            self.square, self.square)
                pygame.draw.rect(self.surface, color=fill,
                                    rect=rect)
                pygame.draw.rect(self.surface, color=black,
                                        rect=rect, width=1)
        
            font_size = round(min(self.x_bounds[0], self.y_bounds[0]) * 0.5)
            text_display = "Current player: " + str(game.turn)
            font = pygame.font.SysFont('Arial', font_size)
            font.set_bold(True)
            text = font.render(text_display, True, player_colors[int(game.turn - 1)])
            self.surface.blit(text, ((self.x_bounds[0] + self.x_bounds[1])/2, round(self.y_bounds[1])))



    def event_loop(self, game: Reversi) -> None:
        """
        Handles user interactions
        Parameters: none beyond self
        Returns: nothing
        """
        while True:
            # Process Pygame events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if not game.done and event.type == pygame.MOUSEBUTTONUP:
                    curr_pos = pygame.mouse.get_pos()
                    self.where_mouse(curr_pos)
                    if self.in_grid:
                        curr_cell = self.cell_loc(curr_pos[0], curr_pos[1])
                        if curr_cell in game.available_moves:
                            try:
                                game.apply_move(curr_cell) #switches player + updates grid
                                # Send the updated game state to the Flask API
                                self.send_game_state(game.get_state())
                            except ValueError:
                                print("This position does not work. Try again!")

                self.draw_window(game)
                pygame.display.update()
                self.clock.tick(24) 

    def send_game_state(self, game_state):
        # Make an HTTP POST request to the Flask API endpoint to update the game state
        # Example:
        response = requests.post('https://othello-sk.herokuapp.com/api/update_game_state', json=game_state)
        if response.status_code != 200:
            return ValueError



@click.command(name="reversi-gui")
@click.option("-s", "--board-size", type=click.INT, default=8, help = "Board Size")
@click.option("-n", "--num-players", type=click.INT, default=2, help = "Number of Players")
@click.option("--othello/--non-othello", default=True, help = "Othello")

def cmd(board_size, num_players, othello): 
    try:
        board = Reversi(board_size, num_players, othello)
        gui_it: GUI_it = GUI_it(game = board)


        pygame_thread = threading.Thread(target=pygame_event_loop, args=(board,))
        pygame_thread.daemon = True  # Allow the thread to exit when the main program exits
        pygame_thread.start()

        gui_it.event_loop(board)
    except ValueError:
        print("Input is invalid")
        return


if __name__ == "__main__":
    cmd()
