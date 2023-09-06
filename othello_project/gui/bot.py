from abc import abstractmethod
from reversi import Reversi, Board, ReversiPiece
from typing import List, Tuple, Optional, Union
import sys
import random
import click

def initiate_game(s: int, p: int, o:bool) -> Reversi: 
    """ 
    Returns a new reversi board game.
    """
    reversi = Reversi(side=s, players=p, othello=o)
    return reversi


class BotBase(ReversiPiece):
    """ 
    Abstract Base Class for a Bot player.
    """
    player: int

    def __init__(self, player: int):

        """
        Constructor

        Args:
            player: integer number of a specific player

        """
        super().__init__(player)
        self.wins = 0
        self.ties = 0
    
    @abstractmethod
    def strategy(self, moves: list, board: Reversi) -> None:
        """
        The strategy of a particular bot. 
        """
        raise NotImplementedError


class RandomBot(BotBase): 
    """ 
    Class for a Bot that plays the 'random' strategy. 
    """
    player: int

    def __init__(self, player: int):
        super().__init__(player)

    def strategy(self, moves: list, board) -> None:
        """ 
        Plays a random move from the current avialable moves on the board.
        """

        move = random.choice(moves)
        board.apply_move(move)
        
class SmartBot(BotBase): 
    """ 
    Class for a Bot that plays the smart 'heuristic' strategy. 
    """
    player: int

    def __init__(self, player: int):
        super().__init__(player)
    
    def strategy(self, moves: list, board: Reversi) -> None:
        """ 
        Plays the the move that results in it having the most peices on the board. 
        """
        curr_n = len(board.board.locations(board.turn))
        pos_moves = moves
        best_move = pos_moves[0]
        for move in pos_moves:
            new_board: Reversi = board.simulate_moves([move])
            new_n = len(new_board.board.locations(board.turn))

            if new_n > curr_n: 
                curr_n = new_n
                best_move = move 

        board.apply_move(best_move)

class SmarterBot(BotBase): 
    """ 
    Class for a Bot that plays the very smart 'heuristic' strategy. 
    """
    player: int

    def __init__(self, player: int):
        super().__init__(player)
    
    def strategy(self, moves, board: Reversi) -> None: 
        """ 
        Plays the move that results either it winning the game, causing the next player to have no possible moves, or 
        in the greatest number of its pieces on the board after the next player has played. 
        """
        pos_moves = moves
        m_values = []
        for move in pos_moves:
            new_board = board.simulate_moves([move])
            
            #Checks if player wins on simulated board, if so applies move. 
            if new_board.outcome == [self.player]: 
                board.apply_move(move)
                return 

            m_value = 0 
            next_ms = new_board.available_moves

            #Checks if opposing player has no moves on new board, if so applies move. 
            if next_ms == []: 
                board.apply_move(move)
                return

            #Else: finds highest m-value and applies the corresponding move. 
            for m in next_ms: 
                n_new_board = new_board.simulate_moves([m])
                count = len(n_new_board.board.locations(self.player))
                m_value += count 
            if next_ms != []: 
                m_value = m_value//len(next_ms)
            m_values.append(m_value)

        highest_m = 0
        ind = 0
        for i, val in enumerate(m_values): 
            if val > highest_m:
                highest_m = val
                ind = i
                 
        board.apply_move(pos_moves[ind])


def constructor(name: str, player: int) -> BotBase:
    """ 
    Contructs the bots playing the game given the user inputs. 

    Args: 
        name: a given type of bot player 
        player: the integer assigned to the bot player 

    Returns: 
        BotBase: A bot player 
    """ 
    if name == "random":
        return RandomBot(player)
    elif name == "smart":
        return SmartBot(player)
    else:
        #name == "very-smart":
        return SmarterBot(player)

### The Game ###
def simulate(reversi: Reversi, number_of_games: int, bots: List[BotBase]) -> None: 
    """ 
    Plays the input number of Reversi games on the given bot.

    Args:
        reversi: A Reversi game 
        number_of_games: the number of games to be played 
        bots: a list of bots playing the game 

    """
    for _ in range(number_of_games): 
        reversi = initiate_game(8, 2, True)
        outcome = reversi.outcome
        while outcome == []: 
            moves = reversi.available_moves_for_player(reversi.turn)
            if moves != []: 
                bot: BotBase = bots[reversi.turn - 1]
                if bot is not None: 
                    bot.strategy(moves, reversi)
            outcome = reversi.outcome

        if len(outcome) == 1:
            bots[outcome[0] - 1].wins += 1

        else: 
            for num in outcome: 
                bots[num - 1].ties += 1

### Click ###
@click.command(name="Reversi-Bot")
@click.option('-n', '--num-games',  type=click.INT, default=100)
@click.option('-1', '--player1',
              type=click.Choice(['random', 'smart', 'very-smart'], case_sensitive=False),
              default="random")
@click.option('-2','--player2',
              type=click.Choice(['random', 'smart', 'very-smart'], case_sensitive=False),
              default="random")

def cmd(num_games, player1, player2):
    """ 
    Click command. 
    """
    board = Reversi(side=8, players=2, othello=True)

    bot1 = constructor(player1, 1)
    bot2 = constructor(player2, 2)

    bots = [bot1, bot2]
    ties = 0 
    simulate(board, num_games, bots)


    for i, player in enumerate(bots): 
        print(f"Player {i + 1} wins: {round((player.wins/num_games) * 100, 2)}%")

    print(f"Ties: {round((bot1.ties/num_games) * 100, 2)}%")


if __name__ == "__main__":
    cmd()





        





