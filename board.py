import pygame

from const import *
from board_dim import BoardDim


class Board:

    def __init__(self, dims=None, linewidth=15, ultimate=False, max=False):
        self.squares = [[0, 0, 0] for row in range(DIM)]
        self.dims = dims

        if not dims:
            self.dims = BoardDim(WIDTH, 0, 0)

        self.linewidth = linewidth
        self.offset = self.dims.sqsize * 0.2
        self.radius = (self.dims.sqsize // 2) * 0.7
        self.max = max

        if ultimate:
            self.create_ultimate()

        self.active = True

    def __str__(self):
        s = ""
        for row in range(DIM):
            for col in range(DIM):
                square = self.squares[row][col]
                s += str(square)
        return s

    def create_ultimate(self):
        for row in range(DIM):
            for col in range(DIM):

                size = self.dims.sqsize
                xcor, ycor = self.dims.xcor + (
                    col * self.dims.sqsize
                ), self.dims.ycor + (row * self.dims.sqsize)
                dims = BoardDim(size=size, xcor=xcor, ycor=ycor)
                linewidth = self.linewidth - 7
                ultimate = self.max

                self.squares[row][col] = Board(
                    dims=dims, linewidth=linewidth, ultimate=ultimate, max=False
                )

    def render(self, surface):
        for row in range(DIM):
            for col in range(DIM):
                square = self.squares[row][col]

                if isinstance(square, Board):
                    square.render(surface)

        # Vertical lines
        pygame.draw.line(
            surface,
            LINE_COLOR,
            (self.dims.xcor + self.dims.sqsize, self.dims.ycor),
            (self.dims.xcor + self.dims.sqsize, self.dims.ycor + self.dims.size),
            self.linewidth,
        )
        pygame.draw.line(
            surface,
            LINE_COLOR,
            (self.dims.xcor + self.dims.size - self.dims.sqsize, self.dims.ycor),
            (
                self.dims.xcor + self.dims.size - self.dims.sqsize,
                self.dims.ycor + self.dims.size,
            ),
            self.linewidth,
        )

        # Horizontal lines
        pygame.draw.line(
            surface,
            LINE_COLOR,
            (self.dims.xcor, self.dims.ycor + self.dims.sqsize),
            (self.dims.xcor + self.dims.size, self.dims.ycor + self.dims.sqsize),
            self.linewidth,
        )
        pygame.draw.line(
            surface,
            LINE_COLOR,
            (self.dims.xcor, self.dims.ycor + self.dims.size - self.dims.sqsize),
            (
                self.dims.xcor + self.dims.size,
                self.dims.ycor + self.dims.size - self.dims.sqsize,
            ),
            self.linewidth,
        )

    def valid_square(self, xclick, yclick):

        row = yclick // self.dims.sqsize
        col = xclick // self.dims.sqsize

        if row > 2:
            row %= DIM
        if col > 2:
            col %= DIM

        square = self.squares[row][col]

        # Base case
        if not isinstance(square, Board):
            return square == 0 and self.active

        # Recursive step
        return square.valid_square(xclick, yclick)

    def mark_square(self, xclick, yclick, player):
        row = yclick // self.dims.sqsize
        col = xclick // self.dims.sqsize

        if row > 2:
            row %= DIM
        if col > 2:
            col %= DIM

        square = self.squares[row][col]

        print("marking -> (", row, col, ")")

        # Base case
        if not isinstance(square, Board):
            self.squares[row][col] = player
            return

        # Recursive step
        square.mark_square(xclick, yclick, player)

    def draw_fig(self, surface, xclick, yclick):
        row = yclick // self.dims.sqsize
        col = xclick // self.dims.sqsize

        if row > 2:
            row %= DIM
        if col > 2:
            col %= DIM

        square = self.squares[row][col]

        # Base case
        if not isinstance(square, Board):

            # Cross
            if square == 1:
                # Descending line
                ipos = (
                    self.dims.xcor + (col * self.dims.sqsize) + self.offset,
                    self.dims.ycor + (row * self.dims.sqsize) + self.offset,
                )
                fpos = (
                    self.dims.xcor + self.dims.sqsize * (1 + col) - self.offset,
                    self.dims.ycor + self.dims.sqsize * (1 + row) - self.offset,
                )
                pygame.draw.line(surface, CROSS_COLOR, ipos, fpos, self.linewidth)

                # Ascending line
                ipos = (
                    self.dims.xcor + (col * self.dims.sqsize) + self.offset,
                    self.dims.ycor + self.dims.sqsize * (1 + row) - self.offset,
                )
                fpos = (
                    self.dims.xcor + self.dims.sqsize * (1 + col) - self.offset,
                    self.dims.ycor + (row * self.dims.sqsize) + self.offset,
                )
                pygame.draw.line(surface, CROSS_COLOR, ipos, fpos, self.linewidth)

            # Circle
            elif square == 2:
                center = (
                    self.dims.xcor + self.dims.sqsize * (0.5 + col),
                    self.dims.ycor + self.dims.sqsize * (0.5 + row),
                )

                pygame.draw.circle(
                    surface, CIRCLE_COLOR, center, self.radius, self.linewidth
                )

            return

        # Recursive step
        square.draw_fig(surface, xclick, yclick)

    def manage_win(self, surface, winner, onmain=False):
        # Transparent screen
        transparent = pygame.Surface((self.dims.size, self.dims.size))
        transparent.set_alpha(ALPHA)
        transparent.fill(FADE)
        if onmain:
            surface.blit(transparent, (self.dims.xcor, self.dims.ycor))
            surface.blit(transparent, (self.dims.xcor, self.dims.ycor))
        surface.blit(transparent, (self.dims.xcor, self.dims.ycor))

        # Draw win
        if not onmain:
            # Cross
            if winner == 1:
                # Descending line
                ipos = (self.dims.xcor + self.offset, self.dims.ycor + self.offset)
                fpos = (
                    self.dims.xcor + self.dims.size - self.offset,
                    self.dims.ycor + self.dims.size - self.offset,
                )
                pygame.draw.line(surface, CROSS_COLOR, ipos, fpos, self.linewidth + 7)

                # Ascending line
                ipos = (
                    self.dims.xcor + self.offset,
                    self.dims.ycor + self.dims.size - self.offset,
                )
                fpos = (
                    self.dims.xcor + self.dims.size - self.offset,
                    self.dims.ycor + self.offset,
                )
                pygame.draw.line(surface, CROSS_COLOR, ipos, fpos, self.linewidth + 7)

            # Circle
            if winner == 2:
                center = (
                    self.dims.xcor + self.dims.size * 0.5,
                    self.dims.ycor + self.dims.size * 0.5,
                )

                pygame.draw.circle(
                    surface,
                    CIRCLE_COLOR,
                    center,
                    self.dims.size * 0.4,
                    self.linewidth + 7,
                )

        # Inactive board
        self.active = False

    def check_draw_win(
        self,
        surface,
    ):

        isfull = True

        for row in range(DIM):
            for col in range(DIM):

                # base case square should have numbers
                square = self.squares[row][col]

                if isinstance(square, Board) and square.active:
                    # other board win
                    winner = square.check_draw_win(surface)
                    if winner:  # recursive step
                        self.squares[row][col] = winner
                        square.manage_win(surface, winner)

                # main
                # vertical wins
                for c in range(DIM):
                    if (
                        self.squares[0][c]
                        == self.squares[1][c]
                        == self.squares[2][c]
                        != 0
                    ):
                        color = CROSS_COLOR if self.squares[0][c] == 1 else CIRCLE_COLOR
                        # draw win
                        ipos = (
                            self.dims.xcor + self.dims.sqsize * (0.5 + c),
                            self.dims.ycor + self.offset,
                        )
                        fpos = (
                            self.dims.xcor + self.dims.sqsize * (0.5 + c),
                            self.dims.ycor + self.dims.size - self.offset,
                        )
                        pygame.draw.line(surface, color, ipos, fpos, self.linewidth)

                        return self.squares[0][c]

                # horizontal wins
                for r in range(DIM):
                    if (
                        self.squares[r][0]
                        == self.squares[r][1]
                        == self.squares[r][2]
                        != 0
                    ):
                        color = CROSS_COLOR if self.squares[r][0] == 1 else CIRCLE_COLOR
                        # draw win
                        ipos = (
                            self.dims.xcor + self.offset,
                            self.dims.ycor + self.dims.sqsize * (r + 0.5),
                        )
                        fpos = (
                            self.dims.xcor + self.dims.size - self.offset,
                            self.dims.ycor + self.dims.sqsize * (r + 0.5),
                        )
                        pygame.draw.line(surface, color, ipos, fpos, self.linewidth)

                        return self.squares[r][0]

                # diagonal wins
                # desc
                if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
                    color = CROSS_COLOR if self.squares[1][1] == 1 else CIRCLE_COLOR
                    # draw win
                    ipos = (self.dims.xcor + self.offset, self.dims.ycor + self.offset)
                    fpos = (
                        self.dims.xcor + self.dims.size - self.offset,
                        self.dims.ycor + self.dims.size - self.offset,
                    )
                    pygame.draw.line(surface, color, ipos, fpos, self.linewidth)

                    return self.squares[1][1]

                # asc
                if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
                    color = CROSS_COLOR if self.squares[1][1] == 1 else CIRCLE_COLOR
                    # draw win
                    ipos = (
                        self.dims.xcor + self.offset,
                        self.dims.ycor + self.dims.size - self.offset,
                    )
                    fpos = (
                        self.dims.xcor + self.dims.size - self.offset,
                        self.dims.ycor + self.offset,
                    )
                    pygame.draw.line(surface, color, ipos, fpos, self.linewidth)

                    return self.squares[1][1]
