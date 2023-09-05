"""
Reversi implementation.

Contains a base class (ReversiBase). You must implement
a Reversi class that inherits from this base class.
"""
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Dict
from copy import deepcopy 

BoardGridType = List[List[Optional[int]]]
"""
Type for representing the state of the game board (the "grid")
as a list of lists. Each entry will either be an integer (meaning
there is a piece at that location for that player) or None,
meaning there is no piece in that location. Players are
numbered from 1.
"""

ListMovesType = List[Tuple[int, int]]
"""
Type for representing lists of moves on the board.
"""

class ReversiBase(ABC):
    """
    Abstract base class for the game of Reversi
    """

    _side: int
    _players: int
    _othello: bool

    def __init__(self, side: int, players: int, othello: bool):
        """
        Constructor

        Args:
            side: Number of squares on each side of the board
            players: Number of players
            othello: Whether to initialize the board with an Othello
            configuration.

        Raises:
            ValueError: If the parity of side and players is incorrect
        """
        self._side = side
        self._players = players
        self._othello = othello

    #
    # PROPERTIES
    #

    @property
    def size(self) -> int:
        """
        Returns the size of the board (the number of squares per side)
        """
        return self._side

    @property
    def num_players(self) -> int:
        """
        Returns the number of players
        """
        return self._players

    @property
    @abstractmethod
    def grid(self) -> BoardGridType:
        """
        Returns the state of the game board as a list of lists.
        Each entry can either be an integer (meaning there is a
        piece at that location for that player) or None,
        meaning there is no piece in that location. Players are
        numbered from 1.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def turn(self) -> int:
        """
        Returns the player number for the player who must make
        the next move (i.e., "whose turn is it?")  Players are
        numbered from 1.

        If the game is over, this property will not return
        any meaningful value.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def available_moves(self) -> ListMovesType:
        """
        Returns the list of positions where the current player
        (as returned by the turn method) could place a piece.

        If the game is over, this property will not return
        any meaningful value.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def done(self) -> bool:
        """
        Returns True if the game is over, False otherwise.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def outcome(self) -> List[int]:
        """
        Returns the list of winners for the game. If the game
        is not yet done, will return an empty list.
        If the game is done, will return a list of player numbers
        (players are numbered from 1). If there is a single winner,
        the list will contain a single integer. If there is a tie,
        the list will contain more than one integer (representing
        the players who tied)
        """
        raise NotImplementedError

    #
    # METHODS
    #

    @abstractmethod
    def piece_at(self, pos: Tuple[int, int]) -> Optional[int]:
        """
        Returns the piece at a given location

        Args:
            pos: Position on the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: If there is a piece at the specified location,
        return the number of the player (players are numbered
        from 1). Otherwise, return None.
        """
        raise NotImplementedError

    @abstractmethod
    def legal_move(self, pos: Tuple[int, int]) -> bool:
        """
        Checks if a move is legal.

        Args:
            pos: Position on the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: If the current player (as returned by the turn
        method) could place a piece in the specified position,
        return True. Otherwise, return False.
        """
        raise NotImplementedError

    @abstractmethod
    def apply_move(self, pos: Tuple[int, int]) -> None:
        """
        Place a piece of the current player (as returned by the turn method) 
        on the board.

        The provided position is assumed to be a legal move (as returned by 
        available_moves, or checked by legal_move). The behaviour of this 
        method when the position is on the board, but is not a legal move, is 
        undefined.

        After applying the move, the turn is updated to the
        next player who can make a move. For example, in a 4
        player game, suppose it is player 1's turn, they
        apply a move, and players 2 and 3 have no possible
        moves, but player 4 does. After player 1's move,
        the turn would be set to 4 (not to 2).

        If, after applying the move, none of the players
        can make a move, the game is over, and the value
        of the turn becomes moot. It cannot be assumed to
        take any meaningful value.

        Args:
            pos: Position on the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: None
        """
        raise NotImplementedError

    @abstractmethod
    def load_game(self, turn: int, grid: BoardGridType) -> None:
        """
        Loads the state of a game, replacing the current
        state of the game.

        Args:
            turn: The player number of the player that
            would make the next move ("whose turn is it?")
            Players are numbered from 1.
            grid: The state of the board as a list of lists
            (same as returned by the grid property)

        Raises:
             ValueError:
             - If the value of turn is inconsistent
               with the _players attribute.
             - If the size of the grid is inconsistent
               with the _side attribute.
             - If any value in the grid is inconsistent
               with the _players attribute.

        Returns: None
        """
        raise NotImplementedError

    @abstractmethod
    def simulate_moves(self,
                       moves: ListMovesType
                       ) -> "ReversiBase":
        """
        Simulates the effect of making a sequence of moves,
        **without** altering the state of the game (instead,
        returns a new object with the result of applying
        the provided moves).

        The provided positions are assumed to be legal
        moves. The behaviour of this method when a
        position is on the board, but is not a legal
        move, is undefined.

        Bear in mind that the number of *turns* involved
        might be larger than the number of moves provided,
        because a player might not be able to make a
        move (in which case, we skip over the player).
        Let's say we provide moves (2,3), (3,2), and (1,2)
        in a 3 player game, that it is player 2's turn,
        and that Player 3 won't be able to make any moves.
        The moves would be processed like this:

        - Player 2 makes move (2, 3)
        - Player 3 can't make any moves
        - Player 1 makes move (3, 2)
        - Player 2 makes move (1, 2)

        Args:
            moves: List of positions, representing moves.

        Raises:
            ValueError: If any of the specified positions
            is outside the bounds of the board.

        Returns: An object of the same type as the object
        the method was called on, reflecting the state
        of the game after applying the provided moves.
        """
        raise NotImplementedError

# class Player:
    
#     name: str 

#     def __init__(self, name) -> None:
#         self.name = name

    
class ReversiPiece: 
    
    def __init__(self, player: int) -> None:
        self._player = player
    
    @property
    def player(self) -> int: 
        """return player associated with the piece"""
        return self._player
    

class Board: 
    
    side: int
    _grid: List[List[Optional[ReversiPiece]]]
    count_pieces: Dict[int, int]

    def __init__(self, side: int) -> None: 
        self._side = side
        self._grid = [[None]*side for _ in range(side)]
        self.count_pieces = {}
    
    @property
    def size(self) -> int:
        """
        Returns the size of the board (the number of squares per side)
        """
        return self._side
    
    @property
    def grid(self) -> BoardGridType:
        printed_board = []
        for row in self._grid:
            print_row: List[Optional[int]] = []
            for cell in row:
                if cell is not None:
                    print_row.append(cell.player)
                else: 
                    print_row.append(None)
            printed_board.append(print_row)
        
        return printed_board
    
    def piece_at(self, pos: Tuple[int, int]) -> Optional[ReversiPiece]:
        r, c = pos
        if not (0 <= r < self.size and 0 <= c < self.size):
            raise ValueError("Position is out of bounds.")
        
        return self._grid[r][c]
    
    def slot_piece(self, location, piece: ReversiPiece) -> None: 
        """
        Places a player at given location on the board (assumes valid location)
        """
        r, c = location 
        existing_piece = self._grid[r][c]
        if existing_piece is not None:
            losing_player: int = existing_piece.player
            self.count_pieces[losing_player] -= 1
        self.count_pieces[piece.player] = (self.count_pieces.get(piece.player, 0) 
                                            + 1)
        self._grid[r][c] = piece
        
    
    def locations(self, p: int) -> List[Tuple[int, int]]: 
        """
        Finds all the locations of a given integer player on the board. 
        """
        locations: List[Tuple[int, int]] = []
        for i, row in enumerate(self._grid): 
            for j, piece in enumerate(row): 
                if piece is not None and piece.player == p: 
                    locations.append((i, j))

        return locations
    
    
class Reversi(ReversiBase):
    _turn : ReversiPiece
    board: Board
    pieces: List[ReversiPiece]
    center: List[Tuple[int, int]]
    
    def __init__(self, side: int, players: int, othello: bool):
        """
        Constructor
        Args:
            side: Number of squares on each side of the board
            players: Number of players
            othello: Whether to initialize the board with an Othello
            configuration.

        Raises:
            ValueError: If the parity of side and players is incorrect or if 
            the othello configuration is true for >2 players 
        """
        super().__init__(side, players, othello)
        
        if players %2 == 0: 
            if side % 2 != 0: 
                raise ValueError("Parity is incorrect (even)")

        if players %2 != 0:
            if side %2 == 0:
                raise ValueError("Parity is incorrect (odd)")
            
        if othello and players != 2:
            raise ValueError("Othello configuration is only valid for 2 \
                players")
        
        self.board = Board(side)
        
        self.pieces = []
        for i in range(1, players + 1):
            self.pieces.append(ReversiPiece(i))

        if othello: 
            n = side//2
            piece1: ReversiPiece = self.pieces[0]
            piece2: ReversiPiece = self.pieces[1]

            self.board.slot_piece((n - 1, n), piece1) #northeast
            self.board.slot_piece((n, n - 1), piece1) #southwest
            self.board.slot_piece((n - 1, n - 1), piece2) #northwest
            self.board.slot_piece((n, n), piece2) #southeast
            
        m: float = (self._side - 1)/2
        half_p: float = self.num_players/2
        self.center = []
        for i in range(self.size):
            for j in range(self.size):
                if abs(i - m) < half_p and abs(j - m) < half_p:
                    self.center.append((i, j))
        
        self._turn = self.pieces[0]

    @property
    def grid(self) -> BoardGridType:
        printed_board = []
        for row in self.board._grid:
            print_row: List[Optional[int]] = []
            for cell in row:
                if cell is not None:
                    print_row.append(cell.player)
                else: 
                    print_row.append(None)
            printed_board.append(print_row)
        
        return printed_board

    @property
    def all_pieces(self) -> List[ReversiPiece]: 
        """
        Returns the list of Pieces used in this game
        """
        return self.pieces

    @property
    def change_turn(self): 
        """
        Changes Turn 
        """
        if self._turn.player == self._players: 
            self._turn = self.pieces[0]
        else: 
            i = self._turn.player
            self._turn = self.pieces[i]

    @property
    def turn(self) -> int:
        t = self._turn
        if t is not None: 
            return t.player
        else:
            return None
        
    
    def available_moves_for_player(self, player: int):
        """
        Returns the list of positions where a given player
        could place a piece.

        If there is no available moves, this function
        will return empty list.
        """
        moves = []
        for r in range(self._side):
            for c in range(self._side):
                if self.legal_move_player_specific((r, c), player):
                    moves.append((r, c))

        return moves

    @property
    def available_moves(self) -> ListMovesType:
        return self.available_moves_for_player(self.turn)

    @property
    def done(self) -> bool:
        for i in range(1, self._players + 1):
            if self.available_moves_for_player(i) != []:
                return False
        
        return True

    @property
    def outcome(self) -> List[int]:
        if self.done: 
            max_pieces = 0
            winners = []
            for i in range(1, self._players + 1):
                if self.piece_counts(i) > max_pieces:
                    max_pieces = self.piece_counts(i)
                    winners = [i]
                elif self.piece_counts(i) == max_pieces:
                    winners.append(i)
            return winners
        else:
            return []
    
    def piece_at(self, pos: Tuple[int, int]) -> Optional[int]:
        cell = self.board.piece_at(pos)
        if cell is not None:
            return cell.player
        else:
            return None

    def legal_move(self, pos: Tuple[int, int]) -> bool:
        return self.legal_move_player_specific(pos, self.turn)
    
    def legal_move_player_specific(self, pos: Tuple[int, int], player: int) \
        -> bool:
        """
        Check if a move is legal.

        Args:
            pos: Position on the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: If the current player (as returned by the turn method) can 
        place a piece in the specified position, return True. 
        Otherwise, return False.
        """
    
        x,y = pos
        if not (0 <= x < self.size and 0 <= y < self.size):
            raise ValueError("Position is out of bounds.")
        
        center_filled = True
        
        for x, y in self.center:
                if self.board.piece_at((y,x)) is None:
                    center_filled = False

        if center_filled:
            return self.legal_move_center_filled(pos, player)
        else:
            return self.legal_move_center_not_filled(pos, self.center)


    def legal_move_center_not_filled(self, pos: Tuple[int, int], 
                                     center: List[Tuple[int, int]]) -> bool:
        """
        Check if a move is legal when the center is not filled.

        Args:
            pos: Position on the board (already checked is legal)
            center: the list of positions on the board that is considered 
                    as the center of the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: If the current player (as returned by the turn method) can 
        place a piece in the specified position, return True. 
        Otherwise, return False.
        """

        x, y = pos
        
        if self.board._grid[x][y] is not None:
            return False
        
        if (x,y) in center:
            return True
        else:
            return False

    def legal_move_center_filled(self, pos: Tuple[int, int], player: int) -> \
        bool:
        """
        Checks if a move is legal for a given player when the center is filled.

        Args:
            pos: Position on the board (already checked is legal)

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: If the current player (as returned by the turn method) can 
        place a piece in the specified position, return True. 
        Otherwise, return False.
        """
        y,x = pos
        legal_dir: List[Optional[Tuple[int, int]]] = []
        exist_dir: bool = False

        if self.board._grid[y][x] is not None:
            return False
            
        directions = [(- 1, 0), (0, 1), (1, 0), (0, -1), 
                        (-1, -1), (-1, 1), 
                        (1, -1), (1, 1)]

        for d1, d2 in directions:
            if 0 <= (y + d1) < self.board.size and 0 <= (x + d2) < \
                self.board.size:
                value = self.board._grid[y + d1][x + d2]
                if value is not None and value.player is not player:
                    legal_dir.append((d1, d2))
    
        if legal_dir != []:
            for coor in legal_dir:
                if coor is not None:
                    d1, d2 = coor
                    r, c = (y + d1, x + d2)
                    if self.valid_dir(d1, d2, r, c, player):
                        exist_dir = True 
            return exist_dir
        else:
            return False
        
    
    def valid_dir(self, d1: int, d2: int, r: int, c: int, player: int) -> bool:
        """
        Helper function for legal_move_center_filled; checks whether move is 
        valid in a particular direction 
        Args:
            d1: row value of direction to check 
            d2: col value of direction to check 
            r: row value of starting pos 
            c: col value of starting pos 

        Returns:
            bool: whether the move is valid in that direction 
        """
        nr, nc = d1 + r, d2 + c
        if not (0 <= (nr) < self.board.size and 0 <= (nc) < self.board.size):
            return False 
        else:
            p = self.board._grid[nr][nc]
            if p is None:
                return False
            elif p.player == player:
                return True
            else: 
                return self.valid_dir(d1, d2, d1 + r, d2 + c, player)

    def apply_move(self, pos: Tuple[int, int]) -> None:
        if not self.legal_move(pos):
            raise ValueError("not a legal move")
        
        r, c = pos
        self.board.slot_piece((r, c), self._turn) 
        
        if not (r, c) in self.center:
            directions = [(- 1, 0), (0, 1), (1, 0), (0, -1), 
                            (-1, -1), (-1, 1), 
                            (1, -1), (1, 1)]
            for a, b in directions:
                start_a, start_b = pos
                while (0 <= (start_a + a) < self.board.size 
                    and 0 <= (start_b + b) < self.board.size):
                    if self.board.piece_at((start_a + a, start_b + b)) == \
                        self._turn:
                        self.flip((r, c), (a, b))
                        break
                    start_a += a
                    start_b += b
        
        if not self.done: 
            self.change_turn
            while self.available_moves_for_player(self.turn) == []:
                self.change_turn
    
    def flip(self, loc: Tuple[int, int], dir: Tuple[int, int]) -> None:
        """
        Takes a location and a direction.
        It changes all the pieces starting from the location 
        in the given direction until there is a piece of the same player 
        as the starting location.
        """
        x, y = loc
        a, b = dir
        wanted_piece: Optional[ReversiPiece] = self.board.piece_at((x, y))

        while self.board.piece_at((x + a, y + b)) != wanted_piece:
            if wanted_piece is not None:
                self.board.slot_piece((x + a, y + b), wanted_piece)
                x += a
                y += b

    def load_game(self, turn: int, grid: BoardGridType) -> None:
        if not 1 <= turn <= self._players:
            raise ValueError("value of turn is inconsistent with the _players \
                attribute.")
        
        if len(grid) != self._side:
            raise ValueError("size of the grid is inconsistent with the _size \
                attribute.")
        
        if len(grid[0]) != self._side:
            raise ValueError("size of the grid is inconsistent with the _size \
                attribute.")
        
        for row in grid:
            for piece in row:
                if piece is not None:
                    if not isinstance(piece, int):
                        raise ValueError("value in the grid is inconsistent \
                            with the _players attribute.")
                    elif not 1 <= piece <= self._players:
                        raise ValueError("value in the grid is inconsistent \
                            with the _players attribute.")
        
        converted_board: List[List[Optional[ReversiPiece]]] = []

        for row in grid:
            converted_row: List[Optional[ReversiPiece]] = []
            for cell in row:
                if cell is not None:
                    self.board.count_pieces[cell] = self.board.count_pieces.get(cell, 0) + 1
                    converted_row.append(self.pieces[cell - 1])
                else: 
                    converted_row.append(None)
            converted_board.append(converted_row)

        self.board._grid = converted_board
        self._turn = self.pieces[turn - 1]

    def simulate_moves(self,
                       moves: ListMovesType
                       ) -> "Reversi":

        new_game = Reversi(side=self._side, players=self._players, \
            othello=self._othello)

        new_game.board = deepcopy(self.board)
        new_game.board._grid = deepcopy(self.board._grid)
        new_game.pieces = deepcopy(self.pieces)
        new_game._turn = deepcopy(self._turn)

        
        for pos in moves:       
            new_game.apply_move(pos)


        return new_game

    def piece_counts(self, player: int) -> int:
        """
        Takes a player and returns how many pieces this player has
        on the board
        
        Args:
            player: the specific player we are studying

        Returns:
            int: the number of pieces the given player has on the board.
        """
        return self.board.count_pieces[player]